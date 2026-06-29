"""
Предопределенные профили настроек для модема
Загружаются из JSON-файлов или используются встроенные
"""

from typing import Dict, List, Optional

from core.modem.config import ModemConfig
from core.modem.profile_loader import ProfileLoader


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
    def stress() -> ModemConfig:
        """Стресс-тест: максимальная нагрузка"""
        return ModemConfig(
            rate=50,
            fhss=4,
            dsss=2,
            attenuation=0
        )

    @staticmethod
    def combat() -> ModemConfig:
        """Боевой режим: FHSS 4 + DSSS 2"""
        return ModemConfig(
            fhss=4,
            dsss=2
        )

    @staticmethod
    def default_tx() -> ModemConfig:
        """Загрузить TX по умолчанию из JSON"""
        config = ProfileLoader.get_tx_config()
        if config:
            return ModemConfig(**config)
        # Fallback на встроенный профиль
        return ModemConfig(
            freq=4000,
            code=11,
            fhss=0,
            dsss=0,
            rate=50,
            attenuation=0,
            address=32923,
            pan=56064,
            ack=1,
            ttl=0,
            trim=111,
            timeslot=0,
            baudrate=420000,
            parity="none",
            stopbits=1,
            inverted=False,
            mode="longrange",
            protocol="crsf"
        )

    @staticmethod
    def default_rx() -> ModemConfig:
        """Загрузить RX по умолчанию из JSON"""
        config = ProfileLoader.get_rx_config()
        if config:
            return ModemConfig(**config)
        # Fallback на встроенный профиль
        return ModemConfig(
            freq=3500,
            code=11,
            fhss=0,
            dsss=0,
            rate=50,
            attenuation=30,
            address=33683,
            pan=56064,
            bind=1111,
            trim=111,
            timeslot=0,
            ewtests=1,
            baudrate=420000,
            parity="none",
            stopbits=1,
            inverted=False,
            mode="longrange",
            protocol="crsf"
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
            "default_tx": Profiles.default_tx(),
            "default_rx": Profiles.default_rx(),
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
