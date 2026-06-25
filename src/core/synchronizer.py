"""
Синхронизация модемов TX и RX
Основа — TX, по нему настраивается RX
"""

from typing import Dict, Optional, Tuple
from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError


class ModemSynchronizer:
    """
    Синхронизация настроек между TX и RX модемами

    Логика:
        1. TX — основа (читаем настройки с TX или из файла)
        2. RX настраивается по TX
        3. bind на RX = address TX
        4. Остальные параметры копируются из TX
        5. rx_overrides применяются поверх
    """

    @staticmethod
    def sync_from_config(
        tx_controller: ModemController,
        rx_controller: ModemController,
        tx_config: Dict,
        rx_overrides: Optional[Dict] = None
    ) -> Tuple[bool, Dict]:
        """
        Синхронизировать модемы на основе конфигурации TX

        Args:
            tx_controller: Контроллер TX модема
            rx_controller: Контроллер RX модема
            tx_config: Настройки для TX (из файла или с модема)
            rx_overrides: Параметры RX, которые отличаются от TX
                         (attenuation, ewtests, address и т.д.)

        Returns:
            Tuple[bool, Dict]: (успех, результаты)
        """
        results = {
            "tx": {},
            "rx": {},
            "sync": {},
            "rx_config_derived": {}
        }

        print("\n" + "=" * 60)
        print("   СИНХРОНИЗАЦИЯ TX → RX")
        print("=" * 60)

        # 1. Применяем конфигурацию к TX
        print("\n🔧 Настройка TX...")
        print(f"   Параметры: freq={tx_config.get('freq')}, address={tx_config.get('address')}")

        try:
            if not tx_controller.is_connected():
                tx_controller.connect()

            tx_results = tx_controller.apply_config(tx_config)
            results["tx"] = tx_results
            tx_controller.disconnect()

            tx_ok = all(
                success for success, _ in tx_results.values()
                if isinstance(success, bool)
            )

            if tx_ok:
                print("   ✅ TX настроен успешно")
            else:
                print("   ❌ Ошибка настройки TX")
                for cmd, (success, response) in tx_results.items():
                    if not success:
                        print(f"      ❌ {cmd}: {response[:50] if response else 'нет ответа'}")
                return False, results

        except ModemConnectionError as e:
            print(f"   ❌ Ошибка подключения TX: {e}")
            return False, results

        # 2. Формируем конфигурацию для RX на основе TX
        print("\n🔧 Формирование конфигурации для RX...")
        rx_config = ModemSynchronizer._derive_rx_config(tx_config, rx_overrides)
        results["rx_config_derived"] = rx_config

        print(f"   freq={rx_config.get('freq')}, bind={rx_config.get('bind')}")
        print(f"   attenuation={rx_config.get('attenuation')}, ewtests={rx_config.get('ewtests')}")

        # 3. Применяем конфигурацию к RX
        print("\n🔧 Настройка RX...")

        try:
            if not rx_controller.is_connected():
                rx_controller.connect()

            rx_results = rx_controller.apply_config(rx_config)
            results["rx"] = rx_results
            rx_controller.disconnect()

            rx_ok = all(
                success for success, _ in rx_results.values()
                if isinstance(success, bool)
            )

            if rx_ok:
                print("   ✅ RX настроен успешно")
            else:
                print("   ❌ Ошибка настройки RX")
                for cmd, (success, response) in rx_results.items():
                    if not success:
                        print(f"      ❌ {cmd}: {response[:50] if response else 'нет ответа'}")
                return False, results

        except ModemConnectionError as e:
            print(f"   ❌ Ошибка подключения RX: {e}")
            return False, results

        # 4. Проверяем синхронизацию
        print("\n🔍 Проверка синхронизации...")
        sync_ok = ModemSynchronizer._verify_sync(
            tx_controller, rx_controller, tx_config, rx_config
        )
        results["sync"]["verified"] = sync_ok

        if sync_ok:
            print("   ✅ Модемы синхронизированы")
        else:
            print("   ⚠️ Не удалось подтвердить синхронизацию")

        print("\n" + "=" * 60)
        return True, results

    @staticmethod
    def sync_from_modem(
        tx_controller: ModemController,
        rx_controller: ModemController,
        rx_overrides: Optional[Dict] = None
    ) -> Tuple[bool, Dict]:
        """
        Синхронизировать модемы: читать настройки с TX модема

        Args:
            tx_controller: Контроллер TX модема
            rx_controller: Контроллер RX модема
            rx_overrides: Параметры RX, которые отличаются от TX

        Returns:
            Tuple[bool, Dict]: (успех, результаты)
        """
        print("\n📖 Чтение настроек с TX модема...")

        try:
            if not tx_controller.is_connected():
                tx_controller.connect()

            tx_config = tx_controller.get_config()
            tx_controller.disconnect()

            if not tx_config:
                print("   ❌ Не удалось прочитать настройки TX")
                return False, {}

            print(f"   ✅ Настройки TX прочитаны")
            print(f"      freq={tx_config.get('freq')}, address={tx_config.get('address')}")
            print(f"      fhss={tx_config.get('fhss')}, dsss={tx_config.get('dsss')}")

            return ModemSynchronizer.sync_from_config(
                tx_controller,
                rx_controller,
                tx_config,
                rx_overrides
            )

        except ModemConnectionError as e:
            print(f"   ❌ Ошибка подключения TX: {e}")
            return False, {}

    @staticmethod
    def _derive_rx_config(tx_config: Dict, rx_overrides: Optional[Dict] = None) -> Dict:
        """
        Сформировать конфигурацию для RX на основе TX

        Логика:
            1. Копируем ВСЕ параметры из TX
            2. Добавляем bind = address TX
            3. Применяем rx_overrides поверх

        Args:
            tx_config: Настройки TX
            rx_overrides: Переопределения для RX

        Returns:
            Dict: Конфигурация для RX
        """
        # 1. Копируем все параметры из TX
        rx_config = tx_config.copy()

        # 2. Добавляем bind = address TX (обязательно)
        if "address" in tx_config:
            rx_config["bind"] = tx_config["address"]
            print(f"   bind = {tx_config['address']} (address TX)")

        # 3. Если есть address в overrides — используем его
        if rx_overrides and "address" in rx_overrides:
            rx_config["address"] = rx_overrides["address"]
            print(f"   address RX = {rx_overrides['address']} (из overrides)")

        # 4. Применяем остальные overrides
        if rx_overrides:
            for key, value in rx_overrides.items():
                if key != "address":  # address уже обработали
                    rx_config[key] = value
                    print(f"   {key} = {value} (из overrides)")

        return rx_config

    @staticmethod
    def _verify_sync(
        tx_controller: ModemController,
        rx_controller: ModemController,
        tx_config: Dict,
        rx_config: Dict
    ) -> bool:
        """
        Проверить, что модемы синхронизированы

        Возвращает:
            bool: True если синхронизация подтверждена
        """
        try:
            # Проверяем TX
            if not tx_controller.is_connected():
                tx_controller.connect()
            tx_info = tx_controller.get_config()
            tx_controller.disconnect()

            # Проверяем RX
            if not rx_controller.is_connected():
                rx_controller.connect()
            rx_info = rx_controller.get_config()
            rx_controller.disconnect()

            if not tx_info or not rx_info:
                print("   ⚠️ Не удалось получить конфигурацию")
                return False

            # Ключевые параметры, которые должны совпадать
            key_params = ["freq", "code", "fhss", "dsss", "rate", "pan", "protocol"]

            all_match = True
            for param in key_params:
                tx_val = tx_info.get(param)
                rx_val = rx_info.get(param)
                if tx_val != rx_val:
                    print(f"   ❌ Не совпадает {param}: TX={tx_val}, RX={rx_val}")
                    all_match = False

            # Проверяем bind
            tx_addr = tx_info.get("address")
            rx_bind = rx_info.get("bind")
            if tx_addr and rx_bind:
                if tx_addr != rx_bind:
                    print(f"   ❌ Не совпадает bind: TX.address={tx_addr}, RX.bind={rx_bind}")
                    all_match = False
                else:
                    print(f"   ✅ bind совпадает: TX.address={tx_addr}, RX.bind={rx_bind}")

            return all_match

        except Exception as e:
            print(f"   ⚠️ Ошибка проверки синхронизации: {e}")
            return False