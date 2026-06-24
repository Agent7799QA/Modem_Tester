"""
Сканер и идентификатор портов модема Салангана-К3
"""

import re
import serial.tools.list_ports
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError


class ModemType(Enum):
    """Тип модема"""
    RX = "RX"
    TX = "TX"
    UNKNOWN = "UNKNOWN"


class PortType(Enum):
    """Тип порта"""
    MANAGEMENT = "management"  # порт управления (115200, команды)
    DATA = "data"  # порт данных (420000, CRSF-поток)
    UNKNOWN = "unknown"  # не удалось определить


@dataclass
class ModemInfo:
    """
    Информация о найденном модеме
    """
    port: str  # COM-порт
    modem_type: ModemType  # RX или TX
    port_type: PortType  # management или data
    version: Optional[str]  # версия прошивки
    serial_number: Optional[str]  # серийный номер
    config: Optional[Dict]  # полная конфигурация (если есть)

    def __repr__(self) -> str:
        return (f"ModemInfo(port={self.port}, "
                f"type={self.modem_type.value}, "
                f"port_type={self.port_type.value})")


class ModemScanner:
    """
    Сканер для обнаружения и идентификации модемов Салангана-К3
    """

    # Константы для идентификации
    PATTERN_MODEM = r"Drone RC \(([A-Z]+)\)"
    PATTERN_VERSION = r"Version:\s*([\d.]+)"
    PATTERN_SN = r"SN:\s*([a-fA-F0-9]+)"
    PATTERN_COMMANDS = r"Commands list:"
    PATTERN_PARAMETERS = r"Current parameters:"
    PATTERN_RADIO = r"Radio:"
    PATTERN_SERIAL = r"Serial:"

    # Время ожидания ответа при сканировании
    SCAN_TIMEOUT = 0.5

    @staticmethod
    def is_modem_response(response: str) -> bool:
        """
        Проверить, является ли ответ ответом от модема

        Args:
            response: Текст ответа

        Returns:
            bool: True если это ответ модема
        """
        return bool(re.search(ModemScanner.PATTERN_MODEM, response))

    @staticmethod
    def get_modem_type(response: str) -> ModemType:
        """
        Определить тип модема по ответу

        Args:
            response: Текст ответа

        Returns:
            ModemType: RX, TX или UNKNOWN
        """
        match = re.search(ModemScanner.PATTERN_MODEM, response)
        if match:
            type_str = match.group(1).upper()
            if type_str == "RX":
                return ModemType.RX
            elif type_str == "TX":
                return ModemType.TX
        return ModemType.UNKNOWN

    @staticmethod
    def is_management_port(response: str) -> bool:
        """
        Проверить, является ли порт портом управления

        Args:
            response: Текст ответа

        Returns:
            bool: True если это порт управления
        """
        if not ModemScanner.is_modem_response(response):
            return False

        # Проверяем наличие характерных маркеров
        has_commands = bool(re.search(ModemScanner.PATTERN_COMMANDS, response))
        has_parameters = bool(re.search(ModemScanner.PATTERN_PARAMETERS, response))
        has_radio = bool(re.search(ModemScanner.PATTERN_RADIO, response))

        return has_commands or has_parameters or has_radio

    @staticmethod
    def extract_version(response: str) -> Optional[str]:
        """
        Извлечь версию прошивки из ответа

        Args:
            response: Текст ответа

        Returns:
            Optional[str]: Версия или None
        """
        match = re.search(ModemScanner.PATTERN_VERSION, response)
        return match.group(1) if match else None

    @staticmethod
    def extract_serial(response: str) -> Optional[str]:
        """
        Извлечь серийный номер из ответа

        Args:
            response: Текст ответа

        Returns:
            Optional[str]: Серийный номер или None
        """
        match = re.search(ModemScanner.PATTERN_SN, response)
        return match.group(1) if match else None

    @staticmethod
    def scan_port(port: str, timeout: float = SCAN_TIMEOUT) -> Optional[ModemInfo]:
        """
        Сканировать один COM-порт для определения модема

        Args:
            port: Имя порта (например "COM3")
            timeout: Таймаут для команды

        Returns:
            Optional[ModemInfo]: Информация о модеме или None
        """
        controller = ModemController(port)

        try:
            # Пытаемся подключиться
            if not controller.connect():
                return None

            # Отправляем help (более информативный, чем print)
            success, response = controller.send_command("help", timeout=timeout)
            controller.disconnect()

            if not success or not response:
                return None

            # Проверяем, что это модем
            if not ModemScanner.is_modem_response(response):
                return None

            # Определяем тип модема
            modem_type = ModemScanner.get_modem_type(response)

            # Определяем тип порта
            port_type = PortType.MANAGEMENT if ModemScanner.is_management_port(response) else PortType.DATA

            # Извлекаем версию и SN
            version = ModemScanner.extract_version(response)
            serial_number = ModemScanner.extract_serial(response)

            # Получаем полную конфигурацию (если это порт управления)
            config = None
            if port_type == PortType.MANAGEMENT:
                # Переподключаемся для print
                if controller.connect():
                    config = controller.get_config()
                    controller.disconnect()

            return ModemInfo(
                port=port,
                modem_type=modem_type,
                port_type=port_type,
                version=version,
                serial_number=serial_number,
                config=config
            )

        except ModemConnectionError:
            return None
        except Exception:
            return None
        finally:
            try:
                controller.disconnect()
            except:
                pass

    @staticmethod
    def scan_all_ports() -> List[ModemInfo]:
        """
        Сканировать все доступные COM-порты

        Returns:
            List[ModemInfo]: Список найденных модемов
        """
        print("\n🔍 Сканирование COM-портов...")

        results = []
        ports = [port.device for port in serial.tools.list_ports.comports()]

        if not ports:
            print("   ❌ COM-порты не найдены")
            return results

        print(f"   Найдено портов: {len(ports)}")

        for port in ports:
            print(f"\n   Проверка {port}...")
            info = ModemScanner.scan_port(port)

            if info:
                print(f"      ✅ Найден модем {info.modem_type.value}")
                print(f"      Тип порта: {info.port_type.value}")
                if info.version:
                    print(f"      Версия: {info.version}")
                if info.serial_number:
                    print(f"      SN: {info.serial_number}")
                results.append(info)
            else:
                print(f"      ❌ Не модем или порт данных")

        return results

    @staticmethod
    def find_modems() -> Dict[str, Optional[str]]:
        """
        Найти TX и RX модемы (для быстрого использования)

        Returns:
            Dict: {"tx": "COMx" or None, "rx": "COMy" or None}
        """
        result = {"tx": None, "rx": None}
        all_modems = ModemScanner.scan_all_ports()

        for info in all_modems:
            if info.port_type == PortType.MANAGEMENT:
                if info.modem_type == ModemType.TX:
                    result["tx"] = info.port
                elif info.modem_type == ModemType.RX:
                    result["rx"] = info.port

        return result

    @staticmethod
    def print_scan_results(results: List[ModemInfo]) -> None:
        """
        Красиво вывести результаты сканирования

        Args:
            results: Список найденных модемов
        """
        if not results:
            print("\n❌ Модемы не найдены")
            return

        print("\n" + "=" * 60)
        print("   РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ")
        print("=" * 60)

        for info in results:
            print(f"\n📌 Порт: {info.port}")
            print(f"   Тип модема: {info.modem_type.value}")
            print(f"   Тип порта: {info.port_type.value}")
            if info.version:
                print(f"   Версия: {info.version}")
            if info.serial_number:
                print(f"   SN: {info.serial_number}")

            # Показываем основные параметры конфигурации
            if info.config and info.port_type == PortType.MANAGEMENT:
                config = info.config
                params = []
                if "freq" in config:
                    params.append(f"freq={config['freq']}")
                if "fhss" in config:
                    params.append(f"fhss={config['fhss']}")
                if "dsss" in config:
                    params.append(f"dsss={config['dsss']}")
                if "rate" in config:
                    params.append(f"rate={config['rate']}")
                if params:
                    print(f"   Параметры: {', '.join(params)}")

    @staticmethod
    def get_modem_info(port: str) -> Optional[ModemInfo]:
        """
        Получить информацию о модеме на конкретном порту

        Args:
            port: Имя COM-порта

        Returns:
            Optional[ModemInfo]: Информация или None
        """
        return ModemScanner.scan_port(port)