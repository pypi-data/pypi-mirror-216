from typing import Sequence, Union

from dependency_injector.containers import Container
from flask_smorest import Blueprint


class MicroApp:
    blueprint: Union[Sequence[Blueprint], Blueprint]
    microapp_container: Container
