"""Модуль управления модемом Салангана-К3"""

from .controller import ModemController
from .config import ModemConfig, ReconnectConfig
from .scanner import ModemScanner, ModemInfo, ModemType, PortType
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
    "ModemScanner",
    "ModemInfo",
    "ModemType",
    "PortType",
    "ModemError",
    "ModemConnectionError",
    "ModemCommandError",
    "ModemTimeoutError",
    "ModemConfigError",
    "ModemNotConnectedError",
]