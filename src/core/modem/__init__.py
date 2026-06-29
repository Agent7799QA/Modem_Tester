"""
Модуль управления модемом Салангана-К3
"""

from .config import ModemConfig, ReconnectConfig
from .controller import ModemController
from .exceptions import *
from .interfaces import IModemController, IModemConfig
from .parameters import ModemParameters, ParamDef
from .port_scanner import ModemInfo, scan_ports, print_modems, find_tx_rx_from_modems
from .profile_loader import ProfileLoader

__all__ = [
    # Основные классы
    "ModemController",
    "ModemConfig",
    "ReconnectConfig",
    "ModemParameters",
    "ParamDef",
    "ModemInfo",
    "ProfileLoader",
    # Функции
    "scan_ports",
    "print_modems",
    "find_tx_rx_from_modems",
    # Интерфейсы
    "IModemController",
    "IModemConfig",
    # Исключения
    "ModemError",
    "ModemConnectionError",
    "ModemCommandError",
    "ModemTimeoutError",
    "ModemConfigError",
    "ModemNotConnectedError",
]
