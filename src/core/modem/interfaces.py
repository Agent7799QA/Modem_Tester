"""
Абстрактные интерфейсы для расширения системы
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional


class IModemController(ABC):
    """Интерфейс управления модемом"""

    @abstractmethod
    def connect(self) -> bool:
        """Подключиться к модему"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Отключиться от модема"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Проверить подключение"""
        pass

    @abstractmethod
    def send_command(self, command: str, timeout: float = 0.5) -> Tuple[bool, str]:
        """
        Отправить команду модему

        Args:
            command: Команда (например "freq 3500")
            timeout: Таймаут ожидания ответа в секундах

        Returns:
            Tuple[bool, str]: (успех, ответ модема)
        """
        pass

    @abstractmethod
    def apply_config(self, config: Dict) -> Dict[str, Tuple[bool, str]]:
        """
        Применить конфигурацию

        Args:
            config: Словарь с настройками

        Returns:
            Dict[команда, (успех, ответ)]
        """
        pass

    @abstractmethod
    def get_config(self, modem_type: str = "TX") -> Dict:
        """Получить текущую конфигурацию модема"""
        pass

    @abstractmethod
    def stat(self) -> Dict:
        """Получить телеметрию через команду stat"""
        pass


class IModemConfig(ABC):
    """Интерфейс конфигурации модема"""

    @abstractmethod
    def to_dict(self) -> Dict:
        """Преобразовать в словарь"""
        pass

    @abstractmethod
    def from_dict(self, data: Dict) -> 'IModemConfig':
        """Загрузить из словаря"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Проверить валидность конфигурации"""
        pass

    @abstractmethod
    def get_commands(self) -> List[str]:
        """Получить список команд для применения"""
        pass