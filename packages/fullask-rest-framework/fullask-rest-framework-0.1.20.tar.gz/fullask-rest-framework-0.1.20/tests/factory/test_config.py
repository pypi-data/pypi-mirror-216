###################
# pytest fixtures #
###################

import json
import os
import tempfile

import pytest

from fullask_rest_framework.factory.app_factory import BaseApplicationFactory

# ##################
# test code starts #
# ##################


def test_load_config_from_envvar_with_kwargs_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "test_config.py")
        with open(path, "w") as test_config:
            test_config.write(
                'API_TITLE = "Crescendo_backend Server API"\n'
                'API_VERSION = "v1"\n'
                'OPENAPI_VERSION = "3.0.0"\n'
                'SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"\n'
            )
            os.environ["TEST_CONFIG"] = path

        with open(path, "r"):

            class TestApplicationFactory(BaseApplicationFactory):
                APP_BASE_DIR = None
                CONFIG_MAPPING = {
                    "test": {
                        "from_envvar": {"variable_name": "TEST_CONFIG"},
                    },
                }
                EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
                MICRO_APP_CONFIG = None

            try:
                TestApplicationFactory.create_app("test")
                assert True
            except Exception as e:
                raise e


def test_load_config_from_envvar_with_args_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "test_config.py")
        with open(path, "w") as test_config:
            test_config.write(
                'API_TITLE = "Crescendo_backend Server API"\n'
                'API_VERSION = "v1"\n'
                'OPENAPI_VERSION = "3.0.0"\n'
                'SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"\n'
            )
            os.environ["TEST_CONFIG"] = path

        with open(path, "r"):

            class TestApplicationFactory(BaseApplicationFactory):
                APP_BASE_DIR = None
                CONFIG_MAPPING = {
                    "test": {
                        "from_envvar": ("TEST_CONFIG",),
                    },
                }
                EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
                MICRO_APP_CONFIG = None

            try:
                TestApplicationFactory.create_app("test")
                assert True
            except Exception as e:
                raise e


def test_load_config_from_prefixed_env_with_kwargs_success():
    os.environ["TESTAPP_API_TITLE"] = "Crescendo_backend Server API"
    os.environ["TESTAPP_API_VERSION"] = "v1"
    os.environ["TESTAPP_OPENAPI_VERSION"] = "3.0.0"
    os.environ["TESTAPP_SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    class TestApplicationFactory(BaseApplicationFactory):
        APP_BASE_DIR = None
        CONFIG_MAPPING = {
            "test": {
                "from_prefixed_env": {"prefix": "TESTAPP"},
            },
        }
        EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
        MICRO_APP_CONFIG = None

    try:
        TestApplicationFactory.create_app("test")
        assert True
    except Exception as e:
        raise e


def test_load_config_from_prefixed_env_with_args_success():
    os.environ["TESTAPP_API_TITLE"] = "Crescendo_backend Server API"
    os.environ["TESTAPP_API_VERSION"] = "v1"
    os.environ["TESTAPP_OPENAPI_VERSION"] = "3.0.0"
    os.environ["TESTAPP_SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    class TestApplicationFactory(BaseApplicationFactory):
        APP_BASE_DIR = None
        CONFIG_MAPPING = {
            "test": {
                "from_prefixed_env": ("TESTAPP",),
            },
        }
        EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
        MICRO_APP_CONFIG = None

    try:
        TestApplicationFactory.create_app("test")
        assert True
    except Exception as e:
        raise e


def test_load_config_from_pyfile_with_kwargs_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "test_config.py")
        with open(path, "w") as test_config:
            test_config.write(
                'API_TITLE = "Crescendo_backend Server API"\n'
                'API_VERSION = "v1"\n'
                'OPENAPI_VERSION = "3.0.0"\n'
                'SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"\n'
            )
        with open(path, "r"):

            class TestApplicationFactory(BaseApplicationFactory):
                APP_BASE_DIR = None
                CONFIG_MAPPING = {
                    "test": {
                        "from_pyfile": {"filename": path},
                    },
                }
                EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
                MICRO_APP_CONFIG = None

            try:
                TestApplicationFactory.create_app("test")
                assert True
            except Exception as e:
                raise e


def test_load_config_from_pyfile_with_args_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "test_config.py")
        with open(path, "w") as test_config:
            test_config.write(
                'API_TITLE = "Crescendo_backend Server API"\n'
                'API_VERSION = "v1"\n'
                'OPENAPI_VERSION = "3.0.0"\n'
                'SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"\n'
            )
        with open(path, "r"):

            class TestApplicationFactory(BaseApplicationFactory):
                APP_BASE_DIR = None
                CONFIG_MAPPING = {
                    "test": {
                        "from_pyfile": (path,),
                    },
                }
                EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
                MICRO_APP_CONFIG = None

            try:
                TestApplicationFactory.create_app("test")
                assert True
            except Exception as e:
                raise e


def test_load_config_from_object_with_kwargs_success():
    class TestConfig:
        API_TITLE = "Crescendo_backend Server API"
        API_VERSION = "v1"
        OPENAPI_VERSION = "3.0.0"
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    class TestApplicationFactory(BaseApplicationFactory):
        APP_BASE_DIR = None
        CONFIG_MAPPING = {
            "test": {
                "from_object": {"obj": TestConfig()},
            },
        }
        EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
        MICRO_APP_CONFIG = None

    try:
        TestApplicationFactory.create_app("test")
        assert True
    except Exception as e:
        raise e


def test_load_config_from_object_with_args_success():
    class TestConfig:
        API_TITLE = "Crescendo_backend Server API"
        API_VERSION = "v1"
        OPENAPI_VERSION = "3.0.0"
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    class TestApplicationFactory(BaseApplicationFactory):
        APP_BASE_DIR = None
        CONFIG_MAPPING = {
            "test": {
                "from_object": (TestConfig(),),
            },
        }
        EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
        MICRO_APP_CONFIG = None

    try:
        TestApplicationFactory.create_app("test")
        assert True
    except Exception as e:
        raise e


def test_load_config_from_file_with_kwargs_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "test_config.json")
        with open(path, "w") as test_config:
            test_config.write(
                """{
                    "API_TITLE": "Crescendo_backend Server API",
                    "API_VERSION": "v1",
                    "OPENAPI_VERSION": "3.0.0",
                    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
                }"""
            )
        with open(path, "r"):

            class TestApplicationFactory(BaseApplicationFactory):
                APP_BASE_DIR = None
                CONFIG_MAPPING = {
                    "test": {
                        "from_file": {"filename": path, "load": json.load},
                    },
                }
                EXTENSION_MODULE = "fullask_rest_framework.factory.extensions"
                MICRO_APP_CONFIG = None

            try:
                TestApplicationFactory.create_app("test")
                assert True
            except Exception as e:
                raise e
