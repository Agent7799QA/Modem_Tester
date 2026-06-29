"""
DTO для конфигурации RX модема
"""

from dataclasses import dataclass
from typing import Dict, Any

from .base import ModemConfigDTO


@dataclass
class RXConfig(ModemConfigDTO):
    """Конфигурация RX модема"""

    # RX-специфичные поля
    bind: int = 1111
    ewtests: int = 0

    def get_commands(self) -> list[str]:
        """Получить список команд для RX"""
        commands = super().get_commands()

        # RX-специфичные команды
        commands.append(f"bind {self.bind}")
        commands.append(f"ewtests {self.ewtests}")

        return commands

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "RXConfig":
        """Создать из JSON-структуры salangan_rx_default.json"""
        config = {}

        # General
        if "General" in json_data:
            config["protocol"] = json_data["General"].get("protocol", "crsf")
            config["led"] = json_data["General"].get("led", "ON")

        # Radio
        if "Radio" in json_data:
            radio = json_data["Radio"]
            config["mode"] = radio.get("mode", "longrange")
            config["rate"] = radio.get("rate", 50)
            config["freq"] = radio.get("freq", 3500)
            config["code"] = radio.get("code", 11)
            config["attenuation"] = radio.get("attenuation", 0)
            config["address"] = radio.get("address", 1111)
            config["pan"] = radio.get("pan", 56064)
            config["trim"] = radio.get("trim", 111)
            config["fhss"] = radio.get("fhss", 0)
            config["dsss"] = radio.get("dsss", 0)
            # RX-специфичные
            config["bind"] = radio.get("bind", 1111)
            config["ewtests"] = radio.get("ewtests", 0)

        # Serial
        if "Serial" in json_data:
            serial = json_data["Serial"]
            config["baudrate"] = serial.get("baudrate", 420000)
            config["parity"] = serial.get("parity", "none")
            config["stopbits"] = serial.get("stopbits", 1)
            config["inverted"] = serial.get("inverted", False)

        # ExternalInterface
        if "ExternalInterface" in json_data:
            ext = json_data["ExternalInterface"]
            config["extmode"] = ext.get("mode", "off")
            config["pin_0_mode"] = ext.get("pin_0_mode", "debug")
            config["pin_0_dependency"] = ext.get("pin_0_dependency", 13)
            config["pin_1_mode"] = ext.get("pin_1_mode", "off")
            config["pin_1_dependency"] = ext.get("pin_1_dependency", 14)

        return cls(**config)