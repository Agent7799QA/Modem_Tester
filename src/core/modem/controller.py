"""
Реализация управления модемом Салангана-К3
"""

import serial
import time
import re
from typing import Dict, Tuple, Optional
from .exceptions import (
    ModemConnectionError,
    ModemCommandError,
    ModemNotConnectedError
)
from .interfaces import IModemController
from .config import ReconnectConfig


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

        # Настройки переподключения
        self.reconnect_config = ReconnectConfig()
        self._reconnect_depth = 0  # счетчик для защиты от зацикливания

    def connect(self) -> bool:
        """
        Подключение к модему

        Returns:
            bool: True если подключение успешно
        """
        self._reconnect_depth = 0  # сбрасываем счетчик при новом подключении

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

    def check_connection(self) -> bool:
        """Проверить, жив ли модем"""
        if not self.is_connected():
            return False
        try:
            success, _ = self.send_command("help", timeout=0.5)
            return success
        except:
            self._is_connected = False
            return False

    def _attempt_reconnect(self) -> bool:
        """
        Попытка переподключиться с экспоненциальной задержкой

        Returns:
            bool: True если переподключились успешно
        """
        if not self.reconnect_config.enabled:
            return False

        self.disconnect()

        for attempt in range(self.reconnect_config.attempts):
            delay = self.reconnect_config.delays[attempt] if attempt < len(self.reconnect_config.delays) else 2.0 ** attempt
            print(f"⚠️ Попытка переподключения {attempt + 1}/{self.reconnect_config.attempts} (ждем {delay:.1f}с)...")
            time.sleep(delay)

            try:
                if self.connect():
                    if self.check_connection():
                        print(f"✅ Переподключение успешно (попытка {attempt + 1})")
                        return True
                    else:
                        print(f"⚠️ Модем не отвечает после подключения")
                else:
                    print(f"⚠️ Не удалось открыть порт")
            except Exception as e:
                print(f"⚠️ Ошибка при переподключении: {e}")

        print(f"❌ Не удалось переподключиться после {self.reconnect_config.attempts} попыток")
        return False

    def send_command(self, command: str, timeout: float = COMMAND_TIMEOUT) -> Tuple[bool, str]:
        """
        Отправить команду модему

        Args:
            command: Команда (например "freq 3500" или "help")
            timeout: Таймаут ожидания ответа

        Returns:
            Tuple[bool, str]: (успех, ответ модема)
        """
        # Проверяем подключение и пытаемся переподключиться если нужно
        if not self.is_connected():
            if not self._attempt_reconnect():
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
            no_data_count = 0
            last_response_len = 0

            while time.time() - start_time < timeout:
                if self._serial.in_waiting:
                    data = self._serial.read(self._serial.in_waiting)
                    response += data.decode('utf-8', errors='ignore')
                    no_data_count = 0
                    last_response_len = len(response)
                else:
                    # Если данных нет, ждем 50 мс и проверяем еще раз
                    time.sleep(0.05)
                    no_data_count += 1
                    # Если дважды подряд не было данных — выходим
                    if no_data_count >= 2 and len(response) > 0:
                        break
                    # Если есть хоть какие-то данные и они не меняются — выходим
                    if len(response) == last_response_len and len(response) > 0:
                        break

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
            print(f"⚠️ Потеря связи с модемом на {self.com_port}: {e}")
            self._is_connected = False
            if self._serial:
                try:
                    self._serial.close()
                except:
                    pass
                self._serial = None

            # Пытаемся переподключиться
            if self.reconnect_config.enabled and self._reconnect_depth < self.reconnect_config.max_retry_per_command:
                self._reconnect_depth += 1
                if self._attempt_reconnect():
                    print("🔄 Повторная отправка команды...")
                    self._reconnect_depth = 0
                    return self.send_command(command, timeout)
                else:
                    self._reconnect_depth = 0
                    raise ModemConnectionError(f"Потеря связи с модемом на {self.com_port}: {e}")
            else:
                raise ModemConnectionError(f"Потеря связи с модемом на {self.com_port}: {e}")

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
            if not self._attempt_reconnect():
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
            "bind",
            "baudrate",
            "parity",
            "stopbits",
            "mode",
            "timeslot",
            "ttl",
            "ack",
            "ewtests",
            "trim",
            "led",
            "max_clients",
            "extmode",
            "extpinmode0",
            "extpindep0",
            "extpinmode1",
            "extpindep1"
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

        # Особый случай: inverted — это toggle
        if "inverted" in config:
            desired = config["inverted"]

            # Получаем текущее состояние
            try:
                current_config = self.get_config()
                current = current_config.get("inverted", False)

                if current != desired:
                    print(f"   🔄 Инверсия: {current} → {desired}")
                    success, response = self.send_command("invert")
                    results["invert"] = (success, response)
                else:
                    results["invert"] = (True, f"already {desired}")
            except Exception as e:
                results["invert"] = (False, str(e))

        return results

    def get_config(self) -> Dict:
        """
        Получить текущую конфигурацию модема (команда print)

        Returns:
            Dict: Словарь с настройками
        """
        if not self.is_connected():
            if not self._attempt_reconnect():
                raise ModemNotConnectedError("Модем не подключен")

        success, response = self.send_command("print", timeout=1.0)

        if not success:
            return {}

        return self._parse_print_output(response)

    def stat(self) -> Dict:
        """
        Получить телеметрию через команду stat

        Returns:
            Dict: Словарь с uplink/downlink RSSI и LQ
        """
        if not self.is_connected():
            if not self._attempt_reconnect():
                raise ModemNotConnectedError("Модем не подключен")

        success, response = self.send_command("stat", timeout=1.0)
        if not success:
            return {}

        return self._parse_stat_output(response)

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
            "freq": r"Central frequency:\s*(\d+)",
            "code": r"Channel code:\s*(\d+)",
            "attenuation": r"Attenuation:\s*(\d+)\s+dB",
            "address": r"Module address:\s*(\d+)",
            "pan": r"Network address:\s*(\d+)",
            "bind": r"Binded address:\s*(\d+)",
            "rate": r"Link rate:\s*(\d+)",
            "fhss": r"FHSS mode:\s*(\d+)",
            "dsss": r"DSSS mode:\s*(\d+)",
            "antenna": r"Antenna:\s+(\w+)",
            "mode": r"Mode:\s*([\w\s]+?)(?:\n|$|\r)",
            "type": r"Drone RC \(([A-Z]+)\)",
            "baudrate": r"Baudrate:\s*(\d+)",
            "parity": r"Parity:\s*(\w+)",
            "stopbits": r"Stop bits:\s*(\d+)",
            "timeslot": r"Time slotting:\s*(\w+)",
            "ttl": r"Retransmissions:\s*(\w+)",
            "ack": r"Acknowledge:\s*(\w+)",
            "ewtests": r"EW tests:\s*(\w+)",
            "trim": r"Crystal trim:\s*(\d+)",
            "led": r"Onboard LED is (ON|OFF)",
            "max_clients": r"Max clients:\s*(\d+)",
            "extmode": r"Interface mode:\s*(\w+)",
            "extpinmode0": r"Pin 0:\s*Mode:\s*(\w+)",
            "extpindep0": r"Pin 0:\s*Dependency:\s*(\d+)",
            "extpinmode1": r"Pin 1:\s*Mode:\s*(\w+)",
            "extpindep1": r"Pin 1:\s*Dependency:\s*(\d+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Преобразуем числа
                if value.isdigit():
                    config[key] = int(value)
                elif value.lower() == "enable":
                    config[key] = 1
                elif value.lower() == "disable" or value.lower() == "disabled":
                    config[key] = 0
                elif value.lower() == "enabled":
                    config[key] = 1
                else:
                    config[key] = value

        # Определяем состояние инверси, led, extmode
        if "led" in config:
            config["led"] = 1 if config["led"] == "ON" else 0
        if "extmode" in config:
            # extmode может быть "off", "bk", "drop", "rssi"
            pass  # оставляем как строку
        if "Not inverted" in output:
            config["inverted"] = False
        elif "Inverted" in output:
            config["inverted"] = True

        return config

    def _parse_stat_output(self, output: str) -> Dict:
        """
        Парсинг вывода команды stat

        Формат:
            Uplink LQ : 100, UplinkRSSI : 94dBm, DownlinkLQ : 100, DownlinkRSSI : 100dBm

        Returns:
            Dict: {
                "uplink_lq": int,
                "uplink_rssi": int,
                "downlink_lq": int,
                "downlink_rssi": int
            }
        """
        result = {}

        # Uplink LQ : 100
        match = re.search(r"Uplink LQ\s*:\s*(\d+)", output)
        if match:
            result["uplink_lq"] = int(match.group(1))

        # UplinkRSSI : 94dBm
        match = re.search(r"UplinkRSSI\s*:\s*(-?\d+)", output)
        if match:
            result["uplink_rssi"] = int(match.group(1))

        # DownlinkLQ : 100
        match = re.search(r"DownlinkLQ\s*:\s*(\d+)", output)
        if match:
            result["downlink_lq"] = int(match.group(1))

        # DownlinkRSSI : 100dBm
        match = re.search(r"DownlinkRSSI\s*:\s*(-?\d+)", output)
        if match:
            result["downlink_rssi"] = int(match.group(1))

        return result

    def __repr__(self) -> str:
        return f"ModemController(port={self.com_port}, connected={self.is_connected()})"