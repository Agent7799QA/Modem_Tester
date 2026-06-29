"""
Загрузка профилей из JSON-файлов
"""

import json
from pathlib import Path
from typing import Dict, Optional, List

from core.dto import TXConfig, RXConfig


class ProfileLoader:
    """
    Загрузчик профилей из JSON-файлов
    """

    TX_DEFAULT_PATH = Path(__file__).parent.parent.parent / "config" / "salangan_tx_default.json"
    RX_DEFAULT_PATH = Path(__file__).parent.parent.parent / "config" / "salangan_rx_default.json"

    @staticmethod
    def load_tx_default() -> Dict:
        """Загрузить сырой JSON TX"""
        path = ProfileLoader.TX_DEFAULT_PATH
        if not path.exists():
            print(f"⚠️ Файл {path} не найден")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def load_rx_default() -> Dict:
        """Загрузить сырой JSON RX"""
        path = ProfileLoader.RX_DEFAULT_PATH
        if not path.exists():
            print(f"⚠️ Файл {path} не найден")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_tx_config() -> TXConfig:
        """Получить TX конфигурацию в виде DTO"""
        data = ProfileLoader.load_tx_default()
        if not data:
            return TXConfig()  # Возвращаем DTO со значениями по умолчанию
        return TXConfig.from_json(data)

    @staticmethod
    def get_rx_config() -> RXConfig:
        """Получить RX конфигурацию в виде DTO"""
        data = ProfileLoader.load_rx_default()
        if not data:
            return RXConfig()  # Возвращаем DTO со значениями по умолчанию
        return RXConfig.from_json(data)

    @staticmethod
    def get_tx_dict() -> Dict:
        """
        Получить TX конфигурацию в виде плоского словаря
        (для обратной совместимости)
        """
        return ProfileLoader.get_tx_config().to_dict()

    @staticmethod
    def get_rx_dict() -> Dict:
        """
        Получить RX конфигурацию в виде плоского словаря
        (для обратной совместимости)
        """
        return ProfileLoader.get_rx_config().to_dict()

    @staticmethod
    def list_names() -> List[str]:
        """Список доступных профилей"""
        return ["tx_default", "rx_default"]

    @staticmethod
    def save_tx_config(config: TXConfig, path: Optional[Path] = None) -> None:
        """Сохранить TX конфигурацию в JSON"""
        if path is None:
            path = ProfileLoader.TX_DEFAULT_PATH

        # Преобразуем DTO в структуру JSON
        data = {
            "General": {
                "protocol": config.protocol,
                "led": config.led,
            },
            "Radio": {
                "mode": config.mode,
                "rate": config.rate,
                "freq": config.freq,
                "code": config.code,
                "attenuation": config.attenuation,
                "address": config.address,
                "pan": config.pan,
                "trim": config.trim,
                "fhss": config.fhss,
                "dsss": config.dsss,
                "timeslot": config.timeslot,
                "ttl": config.ttl,
                "ack": config.ack,
                "max_clients": config.max_clients,
            },
            "Serial": {
                "baudrate": config.baudrate,
                "parity": config.parity,
                "stopbits": config.stopbits,
                "inverted": config.inverted,
            },
            "ExternalInterface": {
                "pin_0_mode": config.pin_0_mode,
                "pin_0_dependency": config.pin_0_dependency,
            }
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def save_rx_config(config: RXConfig, path: Optional[Path] = None) -> None:
        """Сохранить RX конфигурацию в JSON"""
        if path is None:
            path = ProfileLoader.RX_DEFAULT_PATH

        data = {
            "General": {
                "protocol": config.protocol,
                "led": config.led,
            },
            "Radio": {
                "mode": config.mode,
                "rate": config.rate,
                "freq": config.freq,
                "code": config.code,
                "attenuation": config.attenuation,
                "address": config.address,
                "pan": config.pan,
                "trim": config.trim,
                "fhss": config.fhss,
                "dsss": config.dsss,
                "bind": config.bind,
                "ewtests": config.ewtests,
            },
            "Serial": {
                "baudrate": config.baudrate,
                "parity": config.parity,
                "stopbits": config.stopbits,
                "inverted": config.inverted,
            },
            "ExternalInterface": {
                "mode": config.extmode,
                "pin_0_mode": config.pin_0_mode,
                "pin_0_dependency": config.pin_0_dependency,
                "pin_1_mode": config.pin_1_mode,
                "pin_1_dependency": config.pin_1_dependency,
            }
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)