"""Модуль управления модемом Салангана-К3"""

from .controller import ModemController
from .config import ModemConfig, ReconnectConfig
from .port_scanner import ModemInfo
from .exceptions import (
    ModemError,
    ModemConnectionError,
    ModemCommandError,
    ModemTimeoutError,
    ModemConfigError,
    ModemNotConnectedError,
)

__all__ = [
    "ModemController",
    "ModemConfig",
    "ReconnectConfig",
    "ModemInfo",
    "ModemError",
    "ModemConnectionError",
    "ModemCommandError",
    "ModemTimeoutError",
    "ModemConfigError",
    "ModemNotConnectedError",
]