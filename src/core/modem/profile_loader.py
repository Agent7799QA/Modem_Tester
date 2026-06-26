"""
Загрузка профилей из JSON-файлов
"""

import json
from pathlib import Path
from typing import Dict, Optional, List


class ProfileLoader:
    """
    Загрузчик профилей из JSON-файлов
    """

    # Пути к файлам с профилями по умолчанию
    TX_DEFAULT_PATH = "config/salangan_tx_default.json"
    RX_DEFAULT_PATH = "config/salangan_rx_default.json"

    @staticmethod
    def load_tx_default() -> Dict:
        """Загрузить профиль TX по умолчанию"""
        path = Path(ProfileLoader.TX_DEFAULT_PATH)
        if not path.exists():
            print(f"⚠️ Файл {ProfileLoader.TX_DEFAULT_PATH} не найден")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_rx_default() -> Dict:
        """Загрузить профиль RX по умолчанию"""
        path = Path(ProfileLoader.RX_DEFAULT_PATH)
        if not path.exists():
            print(f"⚠️ Файл {ProfileLoader.RX_DEFAULT_PATH} не найден")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_tx_config() -> Dict:
        """Получить конфигурацию TX из JSON"""
        data = ProfileLoader.load_tx_default()
        if not data:
            return {}

        # Извлекаем параметры из структуры JSON
        config = {}

        # General
        if "General" in data:
            if "protocol" in data["General"]:
                config["protocol"] = data["General"]["protocol"]

        # Radio
        if "Radio" in data:
            radio = data["Radio"]
            for key in ["mode", "rate", "timeslot", "ttl", "ack",
                        "freq", "code", "attenuation", "address", "pan",
                        "trim", "fhss", "dsss"]:
                if key in radio:
                    config[key] = radio[key]

        # Serial
        if "Serial" in data:
            serial = data["Serial"]
            for key in ["baudrate", "parity", "stopbits", "inverted"]:
                if key in serial:
                    config[key] = serial[key]

        # ExternalInterface
        if "ExternalInterface" in data:
            ext = data["ExternalInterface"]
            for key in ["extmode", "extpinmode0", "extpindep0", "extpinmode1", "extpindep1"]:
                if key in ext:
                    config[key] = ext[key]

        return config

    @staticmethod
    def get_rx_config() -> Dict:
        """Получить конфигурацию RX из JSON"""
        data = ProfileLoader.load_rx_default()
        if not data:
            return {}

        config = {}

        # General
        if "General" in data:
            if "protocol" in data["General"]:
                config["protocol"] = data["General"]["protocol"]

        # Radio
        if "Radio" in data:
            radio = data["Radio"]
            for key in ["mode", "rate", "freq", "code", "attenuation",
                        "address", "pan", "bind", "trim", "fhss", "dsss", "ewtests"]:
                if key in radio:
                    config[key] = radio[key]

        # Serial
        if "Serial" in data:
            serial = data["Serial"]
            for key in ["baudrate", "parity", "stopbits", "inverted"]:
                if key in serial:
                    config[key] = serial[key]

        # ExternalInterface
        if "ExternalInterface" in data:
            ext = data["ExternalInterface"]
            for key in ["extmode", "extpinmode0", "extpindep0", "extpinmode1", "extpindep1"]:
                if key in ext:
                    config[key] = ext[key]

        return config