"""
DTO для конфигурации TX модема
"""

from dataclasses import dataclass
from typing import Dict, Any

from .base import ModemConfigDTO


@dataclass
class TXConfig(ModemConfigDTO):
    """Конфигурация TX модема"""

    # TX-специфичные поля
    timeslot: int = 0
    ttl: int = 0
    ack: int = 1
    max_clients: int = 1

    def get_commands(self) -> list[str]:
        """Получить список команд для TX"""
        commands = super().get_commands()

        # TX-специфичные команды
        commands.append(f"timeslot {self.timeslot}")
        commands.append(f"ttl {self.ttl}")
        commands.append(f"ack {self.ack}")
        commands.append(f"max_clients {self.max_clients}")

        return commands

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "TXConfig":
        """Создать из JSON-структуры salangan_tx_default.json"""
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
            # TX-специфичные
            config["timeslot"] = radio.get("timeslot", 0)
            config["ttl"] = radio.get("ttl", 0)
            config["ack"] = radio.get("ack", 1)
            config["max_clients"] = radio.get("max_clients", 1)

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
            config["pin_0_mode"] = ext.get("pin_0_mode", "off")
            config["pin_0_dependency"] = ext.get("pin_0_dependency", 13)

        return cls(**config)