"""
Загрузка и сохранение конфигурации модемов из JSON
"""

import json
from typing import Dict, Optional, Any
from pathlib import Path


class ConfigLoader:
    """
    Загрузчик конфигурации из JSON файла
    """

    # Путь к файлу настроек по умолчанию
    DEFAULT_CONFIG_PATH = "config/setup.json"

    @staticmethod
    def load_from_file(filepath: str = None) -> Dict[str, Any]:
        """
        Загрузить конфигурацию из JSON файла

        Args:
            filepath: Путь к файлу (если None — используется DEFAULT_CONFIG_PATH)

        Returns:
            Dict: Словарь с настройками
        """
        if filepath is None:
            filepath = ConfigLoader.DEFAULT_CONFIG_PATH

        path = Path(filepath)
        if not path.exists():
            print(f"⚠️ Файл {filepath} не найден. Создаю дефолтный...")
            ConfigLoader.save_default_config(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_default_config(filepath: str = None):
        """
        Сохранить дефолтную конфигурацию в файл

        Args:
            filepath: Путь к файлу
        """
        if filepath is None:
            filepath = ConfigLoader.DEFAULT_CONFIG_PATH

        # Создаем папку если её нет
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        default_config = {
            "tx_config": {
                "protocol": "crsf",
                "mode": "longrange",
                "rate": 50,
                "timeslot": 0,
                "ttl": 0,
                "ack": 1,
                "freq": 4000,
                "code": 11,
                "attenuation": 0,
                "address": 32923,
                "pan": 56064,
                "trim": 111,
                "fhss": 0,
                "dsss": 0,
                "inverted": False,
                "baudrate": 420000,
                "parity": "none",
                "stopbits": 1
            },
            "rx_config": {
                "protocol": "crsf",
                "mode": "longrange",
                "rate": 50,
                "freq": 3500,
                "code": 11,
                "attenuation": 30,
                "address": 33683,
                "pan": 56064,
                "bind": 1111,
                "trim": 111,
                "fhss": 0,
                "dsss": 0,
                "ewtests": 1,
                "inverted": False,
                "baudrate": 420000,
                "parity": "none",
                "stopbits": 1
            },
            "test": {
                "duration_seconds": 60,
                "interval_seconds": 1,
                "save_results": True
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)

        print(f"✅ Создан дефолтный конфиг: {filepath}")

    @staticmethod
    def save_to_file(config: Dict[str, Any], filepath: str = None):
        """
        Сохранить конфигурацию в JSON файл

        Args:
            config: Словарь с настройками
            filepath: Путь к файлу
        """
        if filepath is None:
            filepath = ConfigLoader.DEFAULT_CONFIG_PATH

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ Конфигурация сохранена: {filepath}")