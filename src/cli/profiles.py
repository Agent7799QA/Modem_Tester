"""
Предопределенные профили настроек для модема
"""

from typing import Dict, List, Optional

from core.dto import TXConfig, RXConfig
from core.modem.profile_loader import ProfileLoader


class Profiles:
    """Предопределенные профили настроек"""

    @staticmethod
    def basic_3500() -> TXConfig:
        """Базовый режим: 3500 МГц, без FHSS/DSSS"""
        return TXConfig(freq=3500, fhss=0, dsss=0)

    @staticmethod
    def basic_4000() -> TXConfig:
        """Базовый режим: 4000 МГц, без FHSS/DSSS"""
        return TXConfig(freq=4000, fhss=0, dsss=0)

    @staticmethod
    def basic_4500() -> TXConfig:
        """Базовый режим: 4500 МГц, без FHSS/DSSS"""
        return TXConfig(freq=4500, fhss=0, dsss=0)

    @staticmethod
    def fhss_full() -> TXConfig:
        """FHSS полный диапазон (3.5, 4.0, 4.5 ГГц)"""
        return TXConfig(fhss=4, dsss=0)

    @staticmethod
    def dsss_full() -> TXConfig:
        """DSSS полный (кодовые каналы 1-24)"""
        return TXConfig(fhss=0, dsss=2)

    @staticmethod
    def stress() -> TXConfig:
        """Стресс-тест: максимальная нагрузка"""
        return TXConfig(rate=50, fhss=4, dsss=2, attenuation=0)

    @staticmethod
    def combat() -> TXConfig:
        """Боевой режим: FHSS 4 + DSSS 2"""
        return TXConfig(fhss=4, dsss=2)

    @staticmethod
    def default_tx() -> TXConfig:
        """Загрузить TX по умолчанию из JSON"""
        return ProfileLoader.get_tx_config()

    @staticmethod
    def default_rx() -> RXConfig:
        """Загрузить RX по умолчанию из JSON"""
        return ProfileLoader.get_rx_config()

    @staticmethod
    def get_all() -> Dict[str, object]:
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
    def get(name: str) -> Optional[object]:
        """Получить профиль по имени"""
        all_profiles = Profiles.get_all()
        return all_profiles.get(name)