from typing import Sequence, Union

from dependency_injector.containers import Container
from flask_smorest import Blueprint


class MicroApp:
    blueprints: Sequence[Blueprint]
    microapp_container: Container
