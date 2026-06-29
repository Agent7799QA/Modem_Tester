"""
Управление параметрами модема Салангана-К3
Единый источник истины для всех параметров
"""

import re
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field

from core.dto import TXConfig, RXConfig, ModemConfigDTO


@dataclass
class ParamDef:
    """Определение параметра"""
    command: str
    description: str
    param_type: str  # "list", "range", "toggle", "string"
    options: Optional[Any] = None
    default: Any = None


class ModemParameters:
    """
    Единый источник информации о параметрах модема
    """

    # ... (COMMON_PARAMS, TX_ONLY_PARAMS, RX_ONLY_PARAMS — без изменений)

    # Паттерны для парсинга print
    PRINT_PATTERNS = {
        "protocol": r"RC protocol:\s+(\w+)",
        "freq": r"Central frequency:\s*(\d+)",
        "code": r"Channel code:\s*(\d+)",
        "attenuation": r"Attenuation:\s*(\d+)\s+dB",
        "address": r"Module address:\s*(\d+)",
        "pan": r"Network address:\s*(\d+)",
        "bind": r"Binded address:\s*(\d+)",
        "rate": r"Link rate:\s*(\d+)",
        "fhss": r"FHSS mode:\s*(\d+)",
        "dsss": r"DSSS mode:\s*(\d+)",
        "mode": r"Mode:\s*([\w\s]+?)(?:\n|$|\r)",
        "type": r"Drone RC \(([A-Z]+)\)",
        "baudrate": r"Baudrate:\s*(\d+)",
        "parity": r"Parity:\s*(\w+)",
        "stopbits": r"Stop bits:\s*(\d+)",
        "timeslot": r"Time slotting:\s*(\w+)",
        "ttl": r"Retransmissions:\s*(\w+)",
        "ack": r"Acknowledge:\s*(\w+)",
        "ewtests": r"EW tests:\s*(\w+)",
        "trim": r"Crystal trim:\s*(\d+)",
        "led": r"Onboard LED is (ON|OFF)",
        "max_clients": r"Max clients:\s*(\d+)",
        "extmode": r"Interface mode:\s*(\w+)",
        "extpinmode0": r"Pin 0:.*?Mode:\s*(\w+)",
        "extpindep0": r"Pin 0:.*?Dependency:\s*(\d+)",
        "extpinmode1": r"Pin 1:.*?Mode:\s*(\w+)",
        "extpindep1": r"Pin 1:.*?Dependency:\s*(\d+)",
    }

    # ... (get_all_params, get_param_names, get_param_def, validate_value, format_options — без изменений)

    @classmethod
    def parse_print_output(cls, output: str, modem_type: str = "TX") -> Union[TXConfig, RXConfig, Dict]:
        """
        Парсинг вывода команды print

        Args:
            output: Ответ модема на команду print
            modem_type: "TX" или "RX"

        Returns:
            TXConfig, RXConfig или Dict (если парсинг не удался)
        """
        from core.modem.profile_loader import ProfileLoader

        # Загружаем конфигурацию по умолчанию для определения целевых ключей
        if modem_type == "TX":
            default_config = ProfileLoader.get_tx_dict()
        else:
            default_config = ProfileLoader.get_rx_dict()

        target_keys = list(default_config.keys()) if default_config else []

        config = {}

        for key, pattern in cls.PRINT_PATTERNS.items():
            if key not in target_keys:
                continue

            if key in ["extpinmode0", "extpindep0", "extpinmode1", "extpindep1"]:
                match = re.search(pattern, output, re.IGNORECASE | re.DOTALL)
            else:
                match = re.search(pattern, output, re.IGNORECASE)

            if match:
                value = match.group(1).strip()
                if value.isdigit():
                    config[key] = int(value)
                elif value.lower() in ["enable", "enabled", "on"]:
                    config[key] = 1
                elif value.lower() in ["disable", "disabled", "off"]:
                    config[key] = 0
                else:
                    config[key] = value

        if "led" in config:
            config["led"] = 1 if config["led"] == "ON" else 0

        if re.search(r"Not\s+inverted", output, re.IGNORECASE):
            config["inverted"] = False
        elif re.search(r"Inverted", output, re.IGNORECASE):
            config["inverted"] = True

        if not config:
            return {}

        # Преобразуем в DTO
        if modem_type == "TX":
            return TXConfig.from_dict(config)
        else:
            return RXConfig.from_dict(config)

    @classmethod
    def parse_print_dict(cls, output: str, modem_type: str = "TX") -> Dict:
        """
        Парсинг вывода команды print в виде словаря (для обратной совместимости)

        Args:
            output: Ответ модема на команду print
            modem_type: "TX" или "RX"

        Returns:
            Dict: Словарь с настройками
        """
        result = cls.parse_print_output(output, modem_type)
        if isinstance(result, dict):
            return result
        return result.to_dict()

    @classmethod
    def parse_stat_output(cls, output: str) -> Dict:
        """Парсинг вывода команды stat (без изменений)"""
        result = {}

        patterns = {
            "uplink_lq": r"Uplink LQ\s*:\s*(\d+)",
            "uplink_rssi": r"UplinkRSSI\s*:\s*(-?\d+)",
            "downlink_lq": r"DownlinkLQ\s*:\s*(\d+)",
            "downlink_rssi": r"DownlinkRSSI\s*:\s*(-?\d+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                result[key] = int(match.group(1))

        return result

    @classmethod
    def get_default_config(cls, modem_type: str) -> Union[TXConfig, RXConfig]:
        """
        Получить конфигурацию по умолчанию для типа модема

        Args:
            modem_type: "TX" или "RX"

        Returns:
            TXConfig или RXConfig
        """
        from core.modem.profile_loader import ProfileLoader

        if modem_type == "TX":
            return ProfileLoader.get_tx_config()
        else:
            return ProfileLoader.get_rx_config()

    @classmethod
    def get_default_dict(cls, modem_type: str) -> Dict:
        """
        Получить конфигурацию по умолчанию в виде словаря (для обратной совместимости)

        Args:
            modem_type: "TX" или "RX"

        Returns:
            Dict: Словарь со значениями по умолчанию
        """
        config = cls.get_default_config(modem_type)
        return config.to_dict()