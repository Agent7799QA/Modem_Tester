"""
Предопределенные профили настроек для модема
"""

from typing import Dict, List, Optional
import json
from pathlib import Path
from modem.config import ModemConfig


class Profiles:
    """Предопределенные профили настроек"""

    @staticmethod
    def basic_3500() -> ModemConfig:
        """Базовый режим: 3500 МГц, без FHSS/DSSS"""
        return ModemConfig(
            freq=3500,
            fhss=0,
            dsss=0
        )

    @staticmethod
    def basic_4000() -> ModemConfig:
        """Базовый режим: 4000 МГц, без FHSS/DSSS"""
        return ModemConfig(
            freq=4000,
            fhss=0,
            dsss=0
        )

    @staticmethod
    def basic_4500() -> ModemConfig:
        """Базовый режим: 4500 МГц, без FHSS/DSSS"""
        return ModemConfig(
            freq=4500,
            fhss=0,
            dsss=0
        )

    @staticmethod
    def fhss_full() -> ModemConfig:
        """FHSS полный диапазон (3.5, 4.0, 4.5 ГГц)"""
        return ModemConfig(
            fhss=4,
            dsss=0
        )

    @staticmethod
    def dsss_full() -> ModemConfig:
        """DSSS полный (кодовые каналы 1-24)"""
        return ModemConfig(
            fhss=0,
            dsss=2
        )

    @staticmethod
    def combat() -> ModemConfig:
        """Боевой режим: FHSS 4 + DSSS 2"""
        return ModemConfig(
            fhss=4,
            dsss=2
        )

    @staticmethod
    def stress() -> ModemConfig:
        """Стресс-тест: максимальная нагрузка"""
        return ModemConfig(
            rate=50,
            fhss=4,
            dsss=2,
            attenuation=0
        )

    @staticmethod
    def get_all() -> Dict[str, ModemConfig]:
        """Получить все предопределенные профили"""
        return {
            "basic_3500": Profiles.basic_3500(),
            "basic_4000": Profiles.basic_4000(),
            "basic_4500": Profiles.basic_4500(),
            "fhss_full": Profiles.fhss_full(),
            "dsss_full": Profiles.dsss_full(),
            "combat": Profiles.combat(),
            "stress": Profiles.stress(),
        }

    @staticmethod
    def list_names() -> List[str]:
        """Получить список имен всех профилей"""
        return list(Profiles.get_all().keys())

    @staticmethod
    def get(name: str) -> Optional[ModemConfig]:
        """Получить профиль по имени"""
        all_profiles = Profiles.get_all()
        return all_profiles.get(name)