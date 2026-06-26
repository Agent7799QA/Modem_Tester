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


    # Получаем путь к корню проекта (src/)
    import os
    TX_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config",
                                   "salangan_tx_default.json")
    RX_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config",
                                   "salangan_rx_default.json")


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

        config = {}

        # General
        if "General" in data:
            if "protocol" in data["General"]:
                config["protocol"] = data["General"]["protocol"]
            if "led" in data["General"]:
                config["led"] = data["General"]["led"]

        # Radio (все ключи)
        if "Radio" in data:
            for key in ["mode", "rate", "timeslot", "ttl", "ack", "max_clients",
                        "freq", "code", "attenuation", "address", "pan", "trim", "fhss", "dsss"]:
                if key in data["Radio"]:
                    config[key] = data["Radio"][key]

        # Serial
        if "Serial" in data:
            for key in ["baudrate", "parity", "stopbits", "inverted"]:
                if key in data["Serial"]:
                    config[key] = data["Serial"][key]

        # ExternalInterface
        if "ExternalInterface" in data:
            for key in ["pin_0_mode", "pin_0_dependency"]:
                if key in data["ExternalInterface"]:
                    config[key] = data["ExternalInterface"][key]

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
            if "led" in data["General"]:
                config["led"] = data["General"]["led"]

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
            for key in ["mode", "pin_0_mode", "pin_0_dependency", "pin_1_mode", "pin_1_dependency"]:
                if key in ext:
                    config[key] = ext[key]

        return config