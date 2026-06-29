"""
Сканер портов для обнаружения модемов Салангана-К3
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import serial.tools.list_ports

from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError


@dataclass
class ModemInfo:
    """Информация о найденном модеме"""
    port: str  # COM-порт
    type: str  # "TX" или "RX"
    config: Dict = field(default_factory=dict)  # параметры из print
    version: Optional[str] = None  # версия прошивки
    serial_number: Optional[str] = None  # серийный номер


def scan_ports() -> List[ModemInfo]:
    """
    Найти все модемы на COM-портах

    Returns:
        List[ModemInfo]: Список найденных модемов
    """
    print("\n🔍 Сканирование COM-портов...")

    result = []
    ports = [p.device for p in serial.tools.list_ports.comports()]

    if not ports:
        print("   ❌ COM-порты не найдены")
        return result

    print(f"   Найдено портов: {len(ports)}")

    for port in ports:
        info = _scan_port(port)
        if info:
            if info.type == "NO_MODEM":
                print(f"   {port}  → ❌ Не модем")
            else:
                print(f"   {port}  → ✅ {info.type}")
            result.append(info)

    return result


def _scan_port(port: str) -> Optional[ModemInfo]:
    """
    Сканировать один порт

    Args:
        port: Имя COM-порта

    Returns:
        Optional[ModemInfo]: Информация о порте
    """
    controller = ModemController(port)

    try:
        if not controller.connect():
            return ModemInfo(port=port, type="NO_MODEM")

        # 1. Отправляем help для проверки
        success, response = controller.send_command("help", timeout=0.5)
        if not success or not response:
            controller.disconnect()
            return ModemInfo(port=port, type="NO_MODEM")

        # 2. Проверяем, что это модем
        is_tx = "Drone RC (TX)" in response
        is_rx = "Drone RC (RX)" in response

        if not is_tx and not is_rx:
            controller.disconnect()
            return ModemInfo(port=port, type="NO_MODEM")

        modem_type = "TX" if is_tx else "RX"

        # 3. Извлекаем версию и SN
        version = _extract_version(response)
        serial_number = _extract_serial(response)

        # 4. Читаем конфигурацию через get_config() с указанием типа
        config = controller.get_config(modem_type)

        controller.disconnect()

        return ModemInfo(
            port=port,
            type=modem_type,
            config=config or {},
            version=version,
            serial_number=serial_number
        )

    except ModemConnectionError:
        return ModemInfo(port=port, type="NO_MODEM")
    except Exception:
        return ModemInfo(port=port, type="NO_MODEM")
    finally:
        try:
            controller.disconnect()
        except:
            pass


def _extract_version(response: str) -> Optional[str]:
    """Извлечь версию прошивки из ответа"""
    match = re.search(r"Version:\s*([\d.]+)", response)
    return match.group(1) if match else None


def _extract_serial(response: str) -> Optional[str]:
    """Извлечь серийный номер из ответа (с поддержкой многострочности)"""
    match = re.search(r"SN:\s*(?:\.\.\s*)?([a-fA-F0-9]{16})", response, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r"([a-fA-F0-9]{16})", response)
    return match.group(1) if match else None


def print_modems(modems: List[ModemInfo]) -> None:
    """
    Вывести результаты сканирования всех портов

    Args:
        modems: Список результатов сканирования
    """
    if not modems:
        print("\n❌ Порты не найдены")
        return

    print("\n" + "=" * 60)
    print("   РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ")
    print("=" * 60)

    for info in modems:
        if info.type == "NO_MODEM":
            print(f"\n📌 Порт: {info.port}  → ❌ Не модем")
        else:
            print(f"\n📌 Порт: {info.port}  → ✅ {info.type}")
            if info.version:
                print(f"   Версия: {info.version}")
            if info.serial_number:
                print(f"   SN: {info.serial_number}")
            if info.config:
                # Используем параметры из ModemParameters для отображения
                params = []
                display_keys = ["freq", "code", "fhss", "dsss", "rate", "address", "bind"]
                for key in display_keys:
                    if key in info.config:
                        params.append(f"{key}={info.config[key]}")
                if params:
                    print(f"   Параметры: {', '.join(params)}")


def find_tx_rx_from_modems(modems: List[ModemInfo]) -> Tuple[Optional[ModemInfo], Optional[ModemInfo]]:
    """
    Найти TX и RX из уже полученного списка модемов

    Args:
        modems: Список найденных модемов

    Returns:
        Tuple[Optional[ModemInfo], Optional[ModemInfo]]: (tx, rx)
    """
    tx = None
    rx = None
    for m in modems:
        if m.type == "TX":
            tx = m
        elif m.type == "RX":
            rx = m
    return tx, rx
