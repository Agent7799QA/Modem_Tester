"""
Сессия для работы с двумя модемами (TX и RX)
"""

import time
import re
import serial.tools.list_ports
from typing import Optional, Dict, Tuple, List
from core.modem.controller import ModemController
from core.modem.config import ModemConfig
from core.modem.exceptions import ModemConnectionError
from core.parser.rx_parser import RxParsingThread
from core.parser.tx_parser import TxParsingThread


class ModemSession:
    """
    Сессия для одновременной работы с TX и RX модемами

    Управляет переключением между режимами конфигурации (115200)
    и CRSF-потоком (420000)
    """

    def __init__(self, tx_com: Optional[str] = None, rx_com: Optional[str] = None):
        """
        Args:
            tx_com: COM-порт для TX модема (если None — автоопределение)
            rx_com: COM-порт для RX модема (если None — автоопределение)
        """
        self.tx_com = tx_com
        self.rx_com = rx_com

        # Контроллеры для конфигурации (115200)
        self.tx_controller: Optional[ModemController] = None
        self.rx_controller: Optional[ModemController] = None

        # Парсеры для CRSF-потока (420000)
        self.tx_parser = TxParsingThread()
        self.rx_parser = RxParsingThread()

        # Состояние сессии
        self._mode = "idle"  # idle | config | streaming
        self._is_configured = False
        self._auto_detected = False

        # Если порты не указаны — запускаем автоопределение
        if tx_com is None or rx_com is None:
            self._auto_detect_ports()

    @staticmethod
    def auto_detect() -> Dict[str, Optional[str]]:
        """
        Автоматическое обнаружение TX и RX модемов

        Returns:
            Dict: {"tx": "COMx" or None, "rx": "COMy" or None}
        """
        print("\n🔍 Автоматическое обнаружение модемов...")

        result = {"tx": None, "rx": None}
        found_tx = []
        found_rx = []

        for port in serial.tools.list_ports.comports():
            port_name = port.device
            print(f"   Проверка {port_name}...")

            try:
                controller = ModemController(port_name)
                if controller.connect():
                    config = controller.get_config()
                    controller.disconnect()

                    if "type" in config:
                        if config["type"] == "TX":
                            found_tx.append(port_name)
                            print(f"      ✅ Найден TX модем на {port_name}")
                        elif config["type"] == "RX":
                            found_rx.append(port_name)
                            print(f"      ✅ Найден RX модем на {port_name}")
                    else:
                        print(f"      ⚠️ Не удалось определить тип на {port_name}")
            except Exception as e:
                # Игнорируем ошибки при сканировании
                pass

        # Определяем результаты
        if len(found_tx) == 1:
            result["tx"] = found_tx[0]
        elif len(found_tx) > 1:
            print(f"      ⚠️ Найдено несколько TX модемов: {found_tx}")
            result["tx"] = found_tx[0]  # Берем первый, пользователь сможет сменить

        if len(found_rx) == 1:
            result["rx"] = found_rx[0]
        elif len(found_rx) > 1:
            print(f"      ⚠️ Найдено несколько RX модемов: {found_rx}")
            result["rx"] = found_rx[0]  # Берем первый

        return result

    def _auto_detect_ports(self) -> None:
        """Автоматическое определение портов с ручным подтверждением"""
        detected = self.auto_detect()

        # Показываем результат
        print("\n📌 Результат автоопределения:")
        print(f"   TX: {detected.get('tx') or 'не найден'}")
        print(f"   RX: {detected.get('rx') or 'не найден'}")

        # Если оба найдены — предлагаем подтвердить
        if detected.get("tx") and detected.get("rx"):
            self.tx_com = detected["tx"]
            self.rx_com = detected["rx"]
            self._auto_detected = True
            print("\n✅ Порты определены автоматически")
            return

        # Если что-то не найдено — переходим к ручному выбору
        print("\n⚠️ Не удалось автоматически определить все порты.")
        self._manual_port_selection()

    def _manual_port_selection(self) -> None:
        """Ручной выбор портов пользователем"""
        from core.user_input import get_two_ports_from_user

        tx, rx = get_two_ports_from_user()
        self.tx_com = tx
        self.rx_com = rx

    def _ensure_controllers(self) -> bool:
        """Создать контроллеры, если порты определены"""
        if not self.tx_com or not self.rx_com:
            print("❌ Порты TX и RX не определены")
            return False

        self.tx_controller = ModemController(self.tx_com)
        self.rx_controller = ModemController(self.rx_com)
        return True

    def configure(self, config: ModemConfig, apply_to_rx: bool = True) -> bool:
        """
        Фаза 1: Применить конфигурацию к модемам через 115200

        Args:
            config: Объект ModemConfig с настройками
            apply_to_rx: Применять ли к RX (если False — только TX)

        Returns:
            bool: True если успешно
        """
        if not self._ensure_controllers():
            return False

        print("\n🔧 Конфигурация модемов...")

        # Для RX добавляем bind = address TX (если не указан)
        rx_config = config.to_dict().copy()
        if apply_to_rx and 'address' in rx_config:
            rx_config['bind'] = rx_config['address']

        # Применяем к TX
        print(f"\n   TX ({self.tx_com}):")
        if not self.tx_controller.connect():
            print("      ❌ Не удалось подключиться к TX")
            return False

        tx_results = self.tx_controller.apply_config(config.to_dict())
        self.tx_controller.disconnect()

        # Проверяем результат TX
        tx_ok = all(success for success, _ in tx_results.values() if isinstance(success, bool))
        if tx_ok:
            print("      ✅ Конфигурация TX применена")
        else:
            print("      ❌ Ошибка при применении конфигурации TX")
            return False

        # Применяем к RX
        if apply_to_rx:
            print(f"\n   RX ({self.rx_com}):")
            if not self.rx_controller.connect():
                print("      ❌ Не удалось подключиться к RX")
                return False

            rx_results = self.rx_controller.apply_config(rx_config)
            self.rx_controller.disconnect()

            rx_ok = all(success for success, _ in rx_results.values() if isinstance(success, bool))
            if rx_ok:
                print("      ✅ Конфигурация RX применена")
            else:
                print("      ❌ Ошибка при применении конфигурации RX")
                return False

        self._is_configured = True
        print("\n✅ Конфигурация завершена")
        return True

    def start_streaming(self, baudrate: int = 420000, inverted: bool = True) -> bool:
        """
        Фаза 2: Запустить CRSF-поток через 420000

        Args:
            baudrate: Скорость порта (420000 или 400000)
            inverted: Инвертировать сигнал

        Returns:
            bool: True если успешно
        """
        if not self._is_configured:
            print("❌ Сначала примените конфигурацию через configure()")
            return False

        if not self.tx_com or not self.rx_com:
            print("❌ Порты не определены")
            return False

        print("\n📡 Запуск CRSF-потока...")

        # Настраиваем и запускаем парсеры
        self.tx_parser.set_port(self.tx_com)
        self.rx_parser.set_port(self.rx_com)

        # Запускаем потоки
        self.tx_parser.start()
        self.rx_parser.start()

        self._mode = "streaming"
        print(f"   ✅ Потоки запущены (TX: {self.tx_com}, RX: {self.rx_com})")
        return True

    def stop_streaming(self) -> None:
        """Остановить CRSF-поток и закрыть порты"""
        print("\n🛑 Остановка CRSF-потока...")

        self.tx_parser.stop()
        self.rx_parser.stop()

        # Ждем завершения потоков
        self.tx_parser.wait()
        self.rx_parser.wait()

        self._mode = "idle"
        print("   ✅ Потоки остановлены")

    def get_telemetry(self) -> Dict:
        """
        Получить текущую телеметрию от парсеров

        Returns:
            Dict: Словарь с RSSI и LQ для downlink/uplink
        """
        # Этот метод будет заполняться на Этапе 4
        return {
            "downlink": {"rssi": None, "lq": None},
            "uplink": {"rssi": None, "lq": None}
        }

    def get_stat(self, modem: str = "rx") -> Dict:
        """
        Получить телеметрию через команду stat (115200)

        Args:
            modem: "tx" или "rx"

        Returns:
            Dict: Словарь с RSSI и LQ
        """
        if self._mode == "streaming":
            print(f"⚠️ Сейчас в режиме streaming, команда stat недоступна")
            return {}

        controller = self.tx_controller if modem == "tx" else self.rx_controller
        com = self.tx_com if modem == "tx" else self.rx_com

        if not controller:
            print(f"❌ Контроллер для {modem} не инициализирован")
            return {}

        try:
            if not controller.connect():
                return {}
            result = controller.stat()
            controller.disconnect()
            return result
        except Exception as e:
            print(f"❌ Ошибка stat: {e}")
            return {}

    @property
    def mode(self) -> str:
        """Текущий режим сессии"""
        return self._mode

    @property
    def is_streaming(self) -> bool:
        """Проверить, запущен ли CRSF-поток"""
        return self._mode == "streaming"

    def __repr__(self) -> str:
        return f"ModemSession(TX={self.tx_com}, RX={self.rx_com}, mode={self._mode})"