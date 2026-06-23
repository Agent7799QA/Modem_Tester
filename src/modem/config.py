"""
Конфигурация модема Салангана-К3
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
import json


@dataclass
class ModemConfig:
    """
    Конфигурация модема Салангана-К3

    Параметры соответствуют документированным командам модема
    """
    # Основные параметры
    protocol: str = "crsf"  # crsf, sbus, mavlink
    freq: int = 3500  # 3500, 4000, 4500, 6500 МГц
    code: int = 11  # 1-24
    attenuation: int = 0  # 0-30 дБ
    address: int = 65535  # 0-65534
    pan: int = 56064  # 0-65534
    rate: int = 50  # 5, 10, 25, 40, 50 Гц

    # Режимы
    fhss: int = 0  # 0-4 (0 - выключен)
    dsss: int = 0  # 0-7 (0 - выключен)
    timeslot: int = 0  # 0 - выключен, 1/2 - слоты

    # Для приемника (опционально)
    bind: Optional[int] = None  # адрес аппаратуры управления

    def to_dict(self) -> Dict:
        """Преобразование в словарь для отправки команд"""
        return {k: v for k, v in asdict(self).items() if v is not None}

    def get_commands(self) -> List[str]:
        """Получить список команд для применения"""
        commands = []

        # Базовые команды
        commands.append(f"protocol {self.protocol}")
        commands.append(f"freq {self.freq}")
        commands.append(f"fhss {self.fhss}")
        commands.append(f"dsss {self.dsss}")
        commands.append(f"code {self.code}")
        commands.append(f"rate {self.rate}")
        commands.append(f"attenuation {self.attenuation}")
        commands.append(f"pan {self.pan}")
        commands.append(f"address {self.address}")

        # Опциональные команды
        if self.bind is not None:
            commands.append(f"bind {self.bind}")

        if self.timeslot > 0:
            commands.append(f"timeslot {self.timeslot}")

        return commands

    def validate(self) -> bool:
        """Проверить валидность параметров"""
        # Проверяем диапазоны
        if self.freq not in [3500, 4000, 4500, 6500]:
            return False
        if not (1 <= self.code <= 24):
            return False
        if not (0 <= self.attenuation <= 30):
            return False
        if not (0 <= self.address <= 65534):
            return False
        if not (0 <= self.pan <= 65534):
            return False
        if self.rate not in [5, 10, 25, 40, 50]:
            return False
        if not (0 <= self.fhss <= 4):
            return False
        if not (0 <= self.dsss <= 7):
            return False
        if self.timeslot not in [0, 1, 2]:
            return False
        if self.protocol not in ["crsf", "sbus", "mavlink"]:
            return False
        return True

    def save(self, filename: str) -> None:
        """Сохранить конфигурацию в JSON файл"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filename: str) -> 'ModemConfig':
        """Загрузить конфигурацию из JSON файла"""
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls(**data)