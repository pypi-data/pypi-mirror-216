import importlib
import inspect
from types import ModuleType
from typing import Any, Dict, List, Optional

from dependency_injector.containers import Container
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from fullask_rest_framework.factory.exceptions import ConfigNotSetError
from fullask_rest_framework.factory.microapp import MicroApp


class BaseApplicationFactory:
    FLASK_APP_NAME: Optional[str] = None
    APP_BASE_DIR: Optional[str] = None
    CONFIG_MAPPING: Optional[dict[str, Any]] = None
    EXTENSION_MODULE: Optional[str] = None
    MICRO_APP_CONFIG: Optional[List[Dict[str, str]]] = None
    DOTENV_SETTINGS: Optional[dict] = None

    @classmethod
    def create_app(cls, environment: str) -> Flask:
        # load environment variables.
        cls._load_dotenv()
        # create a flask app.
        flask_app = cls._create_flask_app()
        # load flask config, with flask app.
        cls._load_config(flask_app=flask_app, environment=environment)
        # create a flask-smorest Api object.
        smorest_api = Api(app=flask_app)
        # configure third-party extensions.
        cls._configure_extensions(flask_app=flask_app)
        # register micro apps. this also does the Dependency Injection.
        cls._register_micro_apps(smorest_api)
        return flask_app

    @classmethod
    def _load_dotenv(cls) -> None:
        """
        load dotenv file, if cls.DOTENV_SETTINGS is set.
        """
        if cls.DOTENV_SETTINGS:
            load_dotenv(**cls.DOTENV_SETTINGS)
            return
        load_dotenv()

    @classmethod
    def _create_flask_app(cls) -> Flask:
        """
        create flask app, with `FLASK_APP_NAME`.
        if cls.__name__ is formatted like "YourCustomAppNameFactory",
        use "YourAppName" instead.
        """
        if cls.FLASK_APP_NAME is not None:
            return Flask(cls.FLASK_APP_NAME)
        elif cls.__name__.endswith("Factory"):
            return Flask(cls.__name__.split("Factory")[0])
        raise AttributeError(
            f"`FLASK_APP_NAME` class variable is not set in '{cls.__name__}'."
            f"set `FLASK_APP_NAME` class variable, or naming the Factory class,"
            f" like '`YourAppName`Factory'."
        )

    @classmethod
    def _load_config(cls, flask_app: Flask, environment: str) -> None:
        # make sure that the CONFIG_MAPPING is set.
        if not cls.CONFIG_MAPPING:
            raise ConfigNotSetError(
                "Config is not set appropriately. Make sure you have assigned the CONFIG class variable"
                "appropriately in your application factory class."
            )
        # make sure that the environment variable is in the CONFIG_MAPPING.keys().
        if environment not in cls.CONFIG_MAPPING.keys():
            raise ValueError(
                f"Environment '{environment}' is not set in the CONFIG_MAPPING."
                f"available environments are: {list(cls.CONFIG_MAPPING.keys())}"
            )

        for key, value in cls.CONFIG_MAPPING[environment].items():
            try:
                config_method = getattr(flask_app.config, key)
            except AttributeError:
                raise ValueError(f"Invalid configuration method: {key}")
            try:
                is_loaded = config_method(**value)
            except TypeError:
                is_loaded = config_method(*value)
            if is_loaded is False:
                raise ValueError(f"Failed to load configuration: {key}")

    @classmethod
    def _configure_extensions(cls, flask_app: Flask) -> None:
        """
        configure third-party extensions, with `EXTENSION_FILE`.
        """

        extensions = cls.get_extensions()
        extension_vars = [
            extension_var
            for extension_var in dir(extensions)
            if not extension_var.startswith("__")
            and not callable(getattr(extensions, extension_var))
        ]
        for var in extension_vars:
            extension_instance = getattr(extensions, var)
            extension_instance.init_app(flask_app)

    @classmethod
    def _register_micro_apps(cls, smorest_api: Api) -> None:
        """
        register micro apps, with cls.MICRO_APP_CONFIG settings.
        this also does the Dependency Injection,
        with dependency_injector's DynamicContainer.
        """
        if not cls.MICRO_APP_CONFIG:
            return
        for micro_app_information in cls.MICRO_APP_CONFIG:
            for app_package_string, url_prefix in micro_app_information.items():
                app_module = importlib.import_module(app_package_string)
                micro_app = next(
                    (
                        cls
                        for name, cls in app_module.__dict__.items()
                        if inspect.isclass(cls)
                        and issubclass(cls, MicroApp)
                        and cls is not MicroApp
                    ),
                    None,
                )
                # Register Blueprint.
                smorest_api.register_blueprint(
                    micro_app.blueprint,
                    url_prefix=url_prefix,
                )
                # get the microapp container.
                cls._setup_di_container(
                    micro_app_container=micro_app.microapp_container
                )

    @classmethod
    def _setup_di_container(cls, micro_app_container: Container) -> None:
        """wiring the DI Container."""
        micro_app_container.wire(packages=[cls.APP_BASE_DIR])

    @classmethod
    def get_extensions(cls) -> ModuleType:
        if cls.EXTENSION_MODULE is not None:
            return importlib.import_module(cls.EXTENSION_MODULE)
        return importlib.import_module("fullask_rest_framework.factory.extensions")
