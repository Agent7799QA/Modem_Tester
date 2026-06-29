"""
Базовый DTO для конфигурации модема
Содержит поля, общие для TX и RX
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ModemConfigDTO:
    """Базовый DTO с общими параметрами модема"""

    # General
    protocol: str = "crsf"
    led: str = "ON"

    # Radio
    mode: str = "longrange"
    rate: int = 50
    freq: int = 3500
    code: int = 11
    attenuation: int = 0
    address: int = 1111
    pan: int = 56064
    trim: int = 111
    fhss: int = 0
    dsss: int = 0

    # Serial
    baudrate: int = 420000
    parity: str = "none"
    stopbits: int = 1
    inverted: bool = False

    # External Interface (общие для TX/RX)
    extmode: str = "off"
    pin_0_mode: str = "debug"
    pin_0_dependency: int = 13
    pin_1_mode: str = "off"
    pin_1_dependency: int = 14

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в плоский словарь"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModemConfigDTO":
        """Создать из плоского словаря"""
        # Фильтруем только те поля, которые есть в DTO
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def get_commands(self) -> list[str]:
        """Получить список команд для применения"""
        commands = []

        # Общие команды
        commands.append(f"protocol {self.protocol}")
        commands.append(f"freq {self.freq}")
        commands.append(f"fhss {self.fhss}")
        commands.append(f"dsss {self.dsss}")
        commands.append(f"code {self.code}")
        commands.append(f"rate {self.rate}")
        commands.append(f"attenuation {self.attenuation}")
        commands.append(f"pan {self.pan}")
        commands.append(f"address {self.address}")
        commands.append(f"baudrate {self.baudrate}")
        commands.append(f"parity {self.parity}")
        commands.append(f"stopbits {self.stopbits}")
        commands.append(f"mode {self.mode}")
        commands.append(f"led {self.led}")

        # Для toggle-команды invert
        if self.inverted:
            commands.append("invert")

        return commands