"""
DTO для конфигураций модемов
"""

from .base import ModemConfigDTO
from .tx_config import TXConfig
from .rx_config import RXConfig

__all__ = [
    "ModemConfigDTO",
    "TXConfig",
    "RXConfig",
]