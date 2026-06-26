"""
Интерактивный редактор параметров модема
"""

import sys
from typing import Dict, List, Optional, Any
from core.modem.controller import ModemController
from core.modem.port_scanner import scan_ports, print_modems
from core.modem.exceptions import ModemConnectionError
from core.modem.parameters import ModemParameters, ParamDef
from core.modem.profile_loader import ProfileLoader


class ModemEditor:
    """
    Интерактивный редактор параметров модема
    Использует ModemParameters как единый источник истины
    """

    @staticmethod
    def get_parameters_for_type(modem_type: str) -> Dict[str, ParamDef]:
        """Получить список параметров для типа модема"""
        return ModemParameters.get_all_params(modem_type)

    @staticmethod
    def detect_modems() -> List[Dict]:
        """Обнаружение всех модемов на COM-портах"""
        print("\n" + "=" * 60)
        print("   ОБНАРУЖЕНИЕ МОДЕМОВ")
        print("=" * 60)

        results = scan_ports()
        print_modems(results)

        modems = []
        for info in results:
            if info.type != "NO_MODEM":
                modem_data = {
                    "port": info.port,
                    "type": info.type,
                    "version": info.version,
                    "sn": info.serial_number,
                    "config": info.config or {}
                }
                modems.append(modem_data)

        print(f"\n✅ Найдено модемов: {len(modems)}")
        return modems

    @staticmethod
    def show_parameters(config: Dict, modem_type: str) -> None:
        """Показать нумерованный список параметров с текущими значениями"""
        print("\n" + "-" * 60)
        print(f"   ТЕКУЩИЕ ПАРАМЕТРЫ ({modem_type})")
        print("-" * 60)

        params = ModemParameters.get_all_params(modem_type)
        idx = 1
        for param_name, param_def in params.items():
            current = config.get(param_name, "не установлен")
            options_str = ModemParameters.format_options(param_name)
            print(f"   {idx:2d}. {param_def.description:30} = {current}  [{options_str}]")
            idx += 1

        print("\n   0. Назад к выбору модема")
        print("-" * 60)

    @staticmethod
    def get_user_choice(prompt: str, max_value: int) -> int:
        """Получить выбор пользователя из нумерованного списка"""
        while True:
            try:
                choice = input(prompt).strip()
                if choice == '0':
                    return 0
                idx = int(choice)
                if 1 <= idx <= max_value:
                    return idx
                print(f"   ❌ Введите число от 1 до {max_value} (или 0 для выхода)")
            except ValueError:
                print("   ❌ Введите число")

    @staticmethod
    def edit_modem(port: str, config: Dict, modem_type: str) -> bool:
        """Редактирование параметров модема"""
        controller = ModemController(port)

        try:
            controller.connect()
            print(f"\n✅ Подключено к {port}")

            changed = False
            params = ModemParameters.get_all_params(modem_type)

            while True:
                ModemEditor.show_parameters(config, modem_type)

                max_idx = len(params)
                choice = ModemEditor.get_user_choice(
                    f"\nВыберите параметр для изменения (1-{max_idx}, 0-назад): ",
                    max_idx
                )

                if choice == 0:
                    print("\n🔙 Возврат к выбору модема...")
                    controller.disconnect()
                    return changed

                param_names = list(params.keys())
                param_name = param_names[choice - 1]
                param_def = params[param_name]

                new_value = ModemEditor._edit_parameter(
                    controller, param_name, param_def, config
                )

                if new_value is not None:
                    config[param_name] = new_value
                    changed = True
                    print(f"\n   ✅ Параметр {param_name} изменен на {new_value}")

            controller.disconnect()
            return changed

        except ModemConnectionError as e:
            print(f"\n❌ Ошибка подключения: {e}")
            return False
        except KeyboardInterrupt:
            print("\n\n⚠️ Прервано пользователем")
            return False
        finally:
            try:
                controller.disconnect()
            except:
                pass

    @staticmethod
    def _edit_parameter(
            controller: ModemController,
            param_name: str,
            param_def: ParamDef,
            config: Dict
    ) -> Optional[Any]:
        """Редактировать один параметр"""
        current = config.get(param_name, "не установлен")
        command = param_def.command

        print(f"\n" + "=" * 50)
        print(f"   ИЗМЕНЕНИЕ: {param_def.description}")
        print("=" * 50)
        print(f"   Текущее значение: {current}")
        print(f"   Команда: {command}")

        if param_def.param_type == "toggle":
            print(f"   Тип: переключатель (toggle)")
            while True:
                choice = input("\n   Изменить инверсию? (y/n): ").strip().lower()
                if choice in ['y', 'yes', 'д', 'да']:
                    success, response = controller.send_command("invert")
                    if success:
                        print("   ✅ Инверсия изменена")
                        new_config = controller.get_config()
                        if new_config:
                            return new_config.get("inverted", current)
                        return not current if isinstance(current, bool) else True
                    else:
                        print(f"   ❌ Ошибка: {response[:50] if response else 'нет ответа'}")
                        return None
                elif choice in ['n', 'no', 'н', 'нет']:
                    return None
                else:
                    print("   ❌ Введите 'y' или 'n'")

        elif param_def.param_type == "list":
            options = param_def.options
            print("\n   Возможные значения:")
            for i, opt in enumerate(options, 1):
                print(f"      {i}. {opt}")

            while True:
                try:
                    choice = input("\n   Выберите новое значение (номер): ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(options):
                        new_value = options[idx]
                        break
                    else:
                        print(f"   ❌ Введите число от 1 до {len(options)}")
                except ValueError:
                    print("   ❌ Введите число")

            cmd = f"{command} {new_value}"
            print(f"\n   Отправка: {cmd}")
            success, response = controller.send_command(cmd)

            if success:
                print("   ✅ Команда выполнена")
                new_config = controller.get_config()
                if new_config and new_config.get(param_name) == new_value:
                    print(f"   ✅ Проверка пройдена: {param_name} = {new_value}")
                    return new_value
                else:
                    print(f"   ⚠️ Не удалось подтвердить изменение")
                    return new_value if new_config else None
            else:
                print(f"   ❌ Ошибка: {response[:50] if response else 'нет ответа'}")
                return None

        elif param_def.param_type == "range":
            min_val = param_def.options["min"]
            max_val = param_def.options["max"]
            print(f"\n   Диапазон: от {min_val} до {max_val}")

            while True:
                try:
                    value = input(f"\n   Введите новое значение ({min_val}-{max_val}): ").strip()
                    new_value = int(value)
                    if min_val <= new_value <= max_val:
                        break
                    else:
                        print(f"   ❌ Введите число от {min_val} до {max_val}")
                except ValueError:
                    print("   ❌ Введите число")

            cmd = f"{command} {new_value}"
            print(f"\n   Отправка: {cmd}")
            success, response = controller.send_command(cmd)

            if success:
                print("   ✅ Команда выполнена")
                new_config = controller.get_config()
                if new_config and new_config.get(param_name) == new_value:
                    print(f"   ✅ Проверка пройдена: {param_name} = {new_value}")
                    return new_value
                else:
                    print(f"   ⚠️ Не удалось подтвердить изменение")
                    return new_value if new_config else None
            else:
                print(f"   ❌ Ошибка: {response[:50] if response else 'нет ответа'}")
                return None

        else:
            print(f"   ❌ Неизвестный тип параметра: {param_def.param_type}")
            return None

    @staticmethod
    def run():
        """Запуск интерактивного редактора"""
        print("\n" + "=" * 60)
        print("   ИНТЕРАКТИВНЫЙ РЕДАКТОР ПАРАМЕТРОВ")
        print("=" * 60)

        while True:
            modems = ModemEditor.detect_modems()

            if not modems:
                print("\n❌ Модемы не найдены")
                return

            print("\n" + "-" * 60)
            print("   ВЫБОР МОДЕМА ДЛЯ РЕДАКТИРОВАНИЯ")
            print("-" * 60)

            for i, modem in enumerate(modems, 1):
                config = modem.get("config", {})
                bind_str = f", bind={config.get('bind', '?')}" if modem['type'] == "RX" else ""
                print(
                    f"   {i}. {modem['port']} ({modem['type']}) - freq={config.get('freq', '?')}, code={config.get('code', '?')}{bind_str}")

            print(f"\n   {len(modems) + 1}. Сравнить параметры TX и RX")
            print(f"   {len(modems) + 2}. Применить настройки по умолчанию")
            print("\n   0. Выход из программы")
            print("-" * 60)

            choice = ModemEditor.get_user_choice(
                f"\nВыберите модем (1-{len(modems)}, {len(modems) + 1}-сравнить, {len(modems) + 2}-настройки по умолчанию, 0-выход): ",
                len(modems) + 2
            )

            if choice == 0:
                print("\nВыход из программы...")
                return

            if choice == len(modems) + 1:
                ModemEditor.compare_modems(modems)
                continue

            if choice == len(modems) + 2:
                ModemEditor.apply_default_settings(modems)
                continue

            selected = modems[choice - 1]
            port = selected["port"]
            config = selected.get("config", {})
            modem_type = selected["type"]

            print(f"\n📌 Редактирование: {port} ({modem_type})")

            changed = ModemEditor.edit_modem(port, config, modem_type)

            if changed:
                print("\n✅ Параметры изменены")
            else:
                print("\nℹ️ Изменений не было")

            print("\n" + "=" * 60)
            print("   ВОЗВРАТ К ВЫБОРУ МОДЕМА")
            print("=" * 60)

    @staticmethod
    def compare_modems(modems: List[Dict]) -> None:
        """Сравнить текущие параметры TX и RX модемов"""
        print("\n" + "=" * 60)
        print("   СРАВНЕНИЕ ПАРАМЕТРОВ TX ↔ RX")
        print("=" * 60)

        tx = None
        rx = None
        for m in modems:
            if m["type"] == "TX":
                tx = m
            elif m["type"] == "RX":
                rx = m

        if not tx or not rx:
            print("\n❌ Для сравнения нужны оба модема (TX и RX)")
            input("\nНажмите Enter для продолжения...")
            return

        tx_config = tx.get("config", {})
        rx_config = rx.get("config", {})

        print(f"\n📌 TX: {tx['port']}")
        print(f"📌 RX: {rx['port']}")

        print("\n" + "-" * 60)
        print("   ПАРАМЕТРЫ СИНХРОНИЗАЦИИ (должны совпадать)")
        print("-" * 60)

        sync_params = [
            ("freq", "Частота (МГц)"),
            ("code", "Кодовый канал"),
            ("fhss", "FHSS режим"),
            ("dsss", "DSSS режим"),
            ("rate", "Скорость (Гц)"),
            ("pan", "Сеть"),
            ("mode", "Режим"),
            ("timeslot", "Временное деление"),
            ("protocol", "Протокол"),
        ]

        all_match = True
        sync_errors = []

        for param, desc in sync_params:
            tx_val = tx_config.get(param, "не установлен")
            rx_val = rx_config.get(param, "не установлен")

            if tx_val == rx_val:
                print(f"   ✅ {desc:18} = {tx_val}")
            else:
                print(f"   ❌ {desc:18} TX={tx_val}, RX={rx_val}")
                all_match = False
                sync_errors.append(f"{desc}: TX={tx_val}, RX={rx_val}")

        print("\n" + "-" * 60)
        print("   ПАРАМЕТРЫ КОНФИГУРАЦИИ (могут различаться)")
        print("-" * 60)

        tx_addr = tx_config.get("address", "не установлен")
        rx_bind = rx_config.get("bind", "не установлен")

        if tx_addr == rx_bind:
            print(f"   ✅ address TX = bind RX = {tx_addr} (совпадают)")
            bind_match = True
        else:
            print(f"   ❌ address TX={tx_addr}, bind RX={rx_bind} (должны совпадать!)")
            bind_match = False
            all_match = False
            sync_errors.append(f"bind: TX.address={tx_addr}, RX.bind={rx_bind}")

        tx_inv = tx_config.get("inverted", "не установлен")
        rx_inv = rx_config.get("inverted", "не установлен")

        if tx_inv != rx_inv:
            print(f"   ✅ inverted: TX={tx_inv}, RX={rx_inv} (различаются — нормально)")
        else:
            print(f"   ⚠️ inverted: TX={tx_inv}, RX={rx_inv} (обычно должны различаться)")

        tx_baud = tx_config.get("baudrate", "не установлен")
        rx_baud = rx_config.get("baudrate", "не установлен")

        if tx_baud != rx_baud:
            print(f"   ✅ baudrate: TX={tx_baud}, RX={rx_baud} (различаются — нормально)")
        else:
            print(f"   ⚠️ baudrate: TX={tx_baud}, RX={rx_baud} (обычно должны различаться)")

        print(f"   ℹ️  address: TX={tx_addr}, RX={rx_config.get('address', 'не установлен')} (у каждого свой)")

        print("\n" + "-" * 60)
        print("   СПЕЦИФИЧНЫЕ ПАРАМЕТРЫ")
        print("-" * 60)

        tx_ack = tx_config.get("ack", "не установлен")
        tx_ttl = tx_config.get("ttl", "не установлен")
        print(f"   TX: ack={tx_ack}, ttl={tx_ttl}")

        rx_ewtests = rx_config.get("ewtests", "не установлен")
        print(f"   RX: ewtests={rx_ewtests}")

        print("\n" + "=" * 60)

        if all_match and bind_match:
            print("   ✅ Модемы СИНХРОНИЗИРОВАНЫ")
            print("   Все параметры совпадают, связь должна работать")
        else:
            print("   ❌ Модемы НЕ СИНХРОНИЗИРОВАНЫ")
            print("\n   Проблемы:")
            for err in sync_errors:
                print(f"      - {err}")

            print("\n   💡 Рекомендации:")
            for err in sync_errors:
                if "bind" in err:
                    print(f"      - Установите RX.bind = TX.address ({tx_addr})")
                elif "freq" in err:
                    print(f"      - Установите одинаковую частоту (freq) на обоих модемах")
                elif "code" in err:
                    print(f"      - Установите одинаковый кодовый канал (code)")
                elif "fhss" in err:
                    print(f"      - Установите одинаковый FHSS режим")
                elif "dsss" in err:
                    print(f"      - Установите одинаковый DSSS режим")
                elif "rate" in err:
                    print(f"      - Установите одинаковую скорость (rate)")
                elif "pan" in err:
                    print(f"      - Установите одинаковую сеть (pan)")
                elif "mode" in err:
                    print(f"      - Установите одинаковый режим (mode)")
                elif "timeslot" in err:
                    print(f"      - Установите одинаковый timeslot")
                elif "protocol" in err:
                    print(f"      - Установите одинаковый протокол (protocol)")

        print("=" * 60)
        input("\nНажмите Enter для продолжения...")

    @staticmethod
    def apply_default_settings(modems: List[Dict]) -> None:
        """Применить настройки по умолчанию ко всем модемам"""
        print("\n" + "=" * 60)
        print("   ПРИМЕНЕНИЕ НАСТРОЕК ПО УМОЛЧАНИЮ")
        print("=" * 60)

        tx = None
        rx = None
        for m in modems:
            if m["type"] == "TX":
                tx = m
            elif m["type"] == "RX":
                rx = m

        if not tx or not rx:
            print("\n❌ Для применения настроек нужны оба модема (TX и RX)")
            input("\nНажмите Enter для продолжения...")
            return

        print(f"\n📌 TX: {tx['port']}")
        print(f"📌 RX: {rx['port']}")

        # Загружаем настройки из JSON-файлов
        tx_config = ProfileLoader.get_tx_config()
        rx_config = ProfileLoader.get_rx_config()

        if not tx_config or not rx_config:
            print("\n❌ Не удалось загрузить настройки по умолчанию")
            print("   Проверьте наличие файлов:")
            print("      - config/salangan_tx_default.json")
            print("      - config/salangan_rx_default.json")
            input("\nНажмите Enter для продолжения...")
            return

        print("\n" + "-" * 60)
        print("   ПАРАМЕТРЫ ПО УМОЛЧАНИЮ")
        print("-" * 60)

        print("\n   TX:")
        for key, value in tx_config.items():
            print(f"      {key}: {value}")

        print("\n   RX:")
        for key, value in rx_config.items():
            print(f"      {key}: {value}")

        print("\n" + "-" * 60)
        confirm = input("\nПрименить настройки по умолчанию? (y/n): ").strip().lower()

        if confirm not in ['y', 'yes', 'д', 'да']:
            print("\n❌ Отмена")
            input("\nНажмите Enter для продолжения...")
            return

        print("\n" + "=" * 60)
        print("   ПРИМЕНЕНИЕ НАСТРОЕК...")
        print("=" * 60)

        success_tx = ModemEditor._apply_config_to_modem(tx['port'], tx_config, "TX")
        success_rx = ModemEditor._apply_config_to_modem(rx['port'], rx_config, "RX")

        print("\n" + "=" * 60)
        if success_tx and success_rx:
            print("   ✅ НАСТРОЙКИ ПО УМОЛЧАНИЮ ПРИМЕНЕНЫ УСПЕШНО!")
        else:
            print("   ❌ Ошибка при применении настроек")
            if not success_tx:
                print(f"      - Не удалось настроить TX ({tx['port']})")
            if not success_rx:
                print(f"      - Не удалось настроить RX ({rx['port']})")
        print("=" * 60)

        input("\nНажмите Enter для продолжения...")

    @staticmethod
    def _apply_config_to_modem(port: str, config: Dict, modem_type: str) -> bool:
        """Применить конфигурацию к модему и проверить результат"""
        controller = ModemController(port)

        try:
            controller.connect()
            print(f"\n✅ Подключено к {port} ({modem_type})")

            param_map = {
                'freq': 'freq', 'code': 'code', 'fhss': 'fhss', 'dsss': 'dsss',
                'rate': 'rate', 'attenuation': 'attenuation', 'address': 'address',
                'pan': 'pan', 'baudrate': 'baudrate', 'parity': 'parity',
                'stopbits': 'stopbits', 'mode': 'mode', 'protocol': 'protocol',
                'timeslot': 'timeslot', 'trim': 'trim', 'invert': 'invert',
                'led': 'led', 'max_clients': 'max_clients',
                'extmode': 'extmode', 'extpinmode0': 'extpinmode0',
                'extpindep0': 'extpindep0', 'extpinmode1': 'extpinmode1',
                'extpindep1': 'extpindep1'
            }

            if modem_type == "TX":
                param_map['ack'] = 'ack'
                param_map['ttl'] = 'ttl'
            else:
                param_map['bind'] = 'bind'
                param_map['ewtests'] = 'ewtests'

            # Формируем команды
            commands = []
            for key, value in config.items():
                if key in param_map:
                    cmd = param_map[key]
                    if isinstance(value, bool):
                        if value:
                            commands.append(cmd)
                    else:
                        commands.append(f"{cmd} {value}")

            # Отправляем команды
            success_count = 0
            for cmd in commands:
                print(f"   → {cmd}")
                success, response = controller.send_command(cmd)
                if success:
                    success_count += 1
                else:
                    print(f"      ❌ Ошибка: {response[:50] if response else 'нет ответа'}")

            # Проверяем, что настройки применились
            print("\n   Проверка применённых настроек...")
            new_config = controller.get_config()
            if not new_config:
                print(f"   ⚠️ Не удалось проверить конфигурацию")
                return False

            # Ключевые параметры для проверки
            key_params = ["freq", "code", "fhss", "dsss", "rate", "attenuation", "address", "pan", "baudrate", "mode",
                          "protocol"]

            if modem_type == "TX":
                key_params.extend(["ack", "ttl"])
            else:
                key_params.extend(["bind", "ewtests"])

            all_match = True
            for key in key_params:
                if key in config:
                    expected = config[key]
                    actual = new_config.get(key)
                    if expected != actual:
                        print(f"      ❌ {key}: ожидалось {expected}, получено {actual}")
                        all_match = False
                    else:
                        print(f"      ✅ {key}: {expected}")

            # Особый случай: inverted (toggle)
            if "inverted" in config:
                expected = config["inverted"]
                actual = new_config.get("inverted", False)
                if expected != actual:
                    print(f"      ❌ inverted: ожидалось {expected}, получено {actual}")
                    all_match = False
                else:
                    print(f"      ✅ inverted: {expected}")

            # Особый случай: led
            if "led" in config:
                expected = config["led"]
                actual = new_config.get("led")
                if expected != actual:
                    print(f"      ❌ led: ожидалось {expected}, получено {actual}")
                    all_match = False
                else:
                    print(f"      ✅ led: {expected}")

            if all_match:
                print(f"\n   ✅ Все параметры проверены и совпадают")
                return True
            else:
                print(f"\n   ⚠️ Некоторые параметры не совпадают")
                return False

        except ModemConnectionError as e:
            print(f"   ❌ Ошибка подключения к {port}: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            return False
        finally:
            try:
                controller.disconnect()
            except:
                pass


if __name__ == "__main__":
    ModemEditor.run()