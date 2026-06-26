"""
Цветной логгер для консоли
"""

from enum import Enum
from typing import Optional


class LogColor(Enum):
    """Цвета для логов"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


class ColoredLogger:
    """Цветной логгер"""

    @staticmethod
    def _colorize(text: str, color: LogColor) -> str:
        """Обернуть текст в цвет"""
        return f"{color.value}{text}{LogColor.RESET.value}"

    @staticmethod
    def info(text: str) -> None:
        """Информационное сообщение (синий)"""
        print(ColoredLogger._colorize(f"ℹ️ {text}", LogColor.BLUE))

    @staticmethod
    def success(text: str) -> None:
        """Успех (зелёный)"""
        print(ColoredLogger._colorize(f"✅ {text}", LogColor.GREEN))

    @staticmethod
    def warning(text: str) -> None:
        """Предупреждение (жёлтый)"""
        print(ColoredLogger._colorize(f"⚠️ {text}", LogColor.YELLOW))

    @staticmethod
    def error(text: str) -> None:
        """Ошибка (красный)"""
        print(ColoredLogger._colorize(f"❌ {text}", LogColor.RED))

    @staticmethod
    def header(text: str, char: str = "=", length: int = 60) -> None:
        """Заголовок (фиолетовый/жирный)"""
        border = ColoredLogger._colorize(char * length, LogColor.CYAN)
        title = ColoredLogger._colorize(f"  {text}  ", LogColor.BOLD | LogColor.HEADER)
        print(f"\n{border}")
        print(title.center(length))
        print(f"{border}\n")

    @staticmethod
    def raw_response(response: str, command: str) -> None:
        """Вывод сырого ответа модема (с рамкой)"""
        border = ColoredLogger._colorize("=" * 60, LogColor.CYAN)
        title = ColoredLogger._colorize(f"📋 ОТВЕТ НА КОМАНДУ: {command}", LogColor.YELLOW)
        print(f"\n{border}")
        print(title)
        print(border)
        print(ColoredLogger._colorize(response, LogColor.GREEN))
        print(f"{border}\n")