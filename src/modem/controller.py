"""
Реализация управления модемом Салангана-К3
"""

import serial
import time
import re
from typing import Dict, Tuple, Optional, List
from .exceptions import (
    ModemConnectionError,
    ModemCommandError,
    ModemTimeoutError,
    ModemNotConnectedError
)
from .interfaces import IModemController


class ModemController(IModemController):
    """
    Контроллер для работы с модемом Салангана-К3
    """

    # Стандартные настройки для модема
    DEFAULT_BAUDRATE = 115200
    DEFAULT_TIMEOUT = 1.0
    COMMAND_TIMEOUT = 0.5

    def __init__(self, com_port: str, baudrate: int = DEFAULT_BAUDRATE):
        """
        Инициализация контроллера

        Args:
            com_port: Имя COM-порта (например "COM3" или "/dev/ttyUSB0")
            baudrate: Скорость обмена (по умолчанию 115200)
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self._serial: Optional[serial.Serial] = None
        self._is_connected = False

    def connect(self) -> bool:
        """
        Подключение к модему

        Returns:
            bool: True если подключение успешно
        """
        try:
            self._serial = serial.Serial(
                port=self.com_port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.DEFAULT_TIMEOUT
            )
            self._is_connected = True
            return True

        except serial.SerialException as e:
            self._is_connected = False
            raise ModemConnectionError(f"Не удалось подключиться к {self.com_port}: {e}")

        except Exception as e:
            self._is_connected = False
            raise ModemConnectionError(f"Ошибка подключения: {e}")

    def disconnect(self) -> None:
        """Отключение от модема"""
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._is_connected = False

    def is_connected(self) -> bool:
        """Проверить, подключены ли к модему"""
        return self._is_connected and self._serial is not None and self._serial.is_open

    def send_command(self, command: str, timeout: float = COMMAND_TIMEOUT) -> Tuple[bool, str]:
        """
        Отправить команду модему

        Args:
            command: Команда (например "freq 3500" или "help")
            timeout: Таймаут ожидания ответа

        Returns:
            Tuple[bool, str]: (успех, ответ модема)
        """
        if not self.is_connected():
            raise ModemNotConnectedError("Модем не подключен")

        try:
            # Очищаем буфер перед отправкой
            self._serial.reset_input_buffer()

            # Отправляем команду с символом новой строки
            cmd = command.strip() + "\n"
            self._serial.write(cmd.encode('utf-8'))

            # Ждем ответ
            time.sleep(0.05)  # Небольшая задержка для обработки

            response = ""
            start_time = time.time()

            while time.time() - start_time < timeout:
                if self._serial.in_waiting:
                    data = self._serial.read(self._serial.in_waiting)
                    response += data.decode('utf-8', errors='ignore')

                    # Проверяем признаки завершения ответа
                    if response.endswith("> ") or response.endswith("> \n"):
                        break
                time.sleep(0.01)

            # Проверяем наличие ошибок в ответе
            if response:
                response_lower = response.lower()
                if "error" in response_lower or "fail" in response_lower:
                    return False, response
                else:
                    return True, response
            else:
                return False, ""

        except serial.SerialException as e:
            self._is_connected = False
            raise ModemCommandError(f"Ошибка при отправке команды: {e}")

        except Exception as e:
            raise ModemCommandError(f"Неизвестная ошибка: {e}")

    def apply_config(self, config: Dict) -> Dict[str, Tuple[bool, str]]:
        """
        Применить конфигурацию к модему

        Args:
            config: Словарь с настройками

        Returns:
            Dict[команда, (успех, ответ)]
        """
        if not self.is_connected():
            raise ModemNotConnectedError("Модем не подключен")

        results = {}

        # Проверяем соединение командой help
        success, response = self.send_command("help", timeout=1.0)
        results["connection_check"] = (success, response)

        if not success:
            return results

        # Порядок применения команд (важен для зависимостей)
        command_order = [
            "protocol",
            "freq",
            "fhss",
            "dsss",
            "code",
            "rate",
            "attenuation",
            "pan",
            "address",
            "bind"
        ]

        for cmd_name in command_order:
            if cmd_name in config:
                value = config[cmd_name]
                cmd = f"{cmd_name} {value}"
                success, response = self.send_command(cmd)
                results[cmd_name] = (success, response)

                # Если команда не удалась, останавливаемся
                if not success:
                    break

        return results

    def get_config(self) -> Dict:
        """
        Получить текущую конфигурацию модема (команда print)

        Returns:
            Dict: Словарь с настройками
        """
        if not self.is_connected():
            raise ModemNotConnectedError("Модем не подключен")

        success, response = self.send_command("print", timeout=1.0)

        if not success:
            return {}

        return self._parse_print_output(response)

    def _parse_print_output(self, output: str) -> Dict:
        """
        Парсинг вывода команды print

        Args:
            output: Вывод команды print

        Returns:
            Dict: Распарсенные настройки
        """
        config = {}

        # Регулярные выражения для парсинга
        patterns = {
            "protocol": r"RC protocol:\s+(\w+)",
            "freq": r"Central frequency:\s+(\d+)",
            "code": r"Channel code:\s+(\d+)",
            "attenuation": r"Attenuation:\s+(\d+)\s+dB",
            "address": r"Module address:\s+(\d+)",
            "pan": r"Network address:\s+(\d+)",
            "bind": r"Binded address:\s+(\d+)",
            "rate": r"Link rate:\s+(\d+)",
            "fhss": r"FHSS mode:\s+(\d+)",
            "dsss": r"DSSS mode:\s+(\d+)",
            "antenna": r"Antenna:\s+(\w+)",
            "mode": r"Mode:\s+(\w+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                value = match.group(1)
                # Преобразуем числа
                if value.isdigit():
                    config[key] = int(value)
                else:
                    config[key] = value

        return config

    def __repr__(self) -> str:
        return f"ModemController(port={self.com_port}, connected={self.is_connected()})"