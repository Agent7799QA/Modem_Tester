"""
Интерактивный редактор параметров модема

Что делает код
Этап	Описание
1. Обнаружение	Сканирует COM-порты, находит модемы, читает print
2. Выбор	Показывает список найденных модемов, пользователь выбирает
3. Редактирование	Показывает все параметры с текущими значениями и вариантами1
4. Изменение	Пользователь выбирает параметр → вводит новое значение
5. Проверка	Отправляет команду → читает print → подтверждает изменение
"""

import sys
from typing import Dict, List, Optional, Any, Tuple
from core.modem.controller import ModemController
from core.modem.port_scanner import ModemScanner, ModemInfo, ModemType, PortType
from core.modem.exceptions import ModemConnectionError


class ModemEditor:
    """
    Интерактивный редактор параметров модема
    """

    # Фиксированная структура параметров для Салангана-К3
    PARAMETERS = {
        "freq": {
            "command": "freq",
            "description": "Central frequency (МГц)",
            "type": "list",
            "options": [3500, 4000, 4500, 6500]
        },
        "code": {
            "command": "code",
            "description": "Channel code",
            "type": "range",
            "options": {"min": 1, "max": 24}
        },
        "fhss": {
            "command": "fhss",
            "description": "FHSS mode",
            "type": "list",
            "options": [0, 1, 2, 3, 4]
        },
        "dsss": {
            "command": "dsss",
            "description": "DSSS mode",
            "type": "list",
            "options": [0, 1, 2, 3, 4, 7]
        },
        "rate": {
            "command": "rate",
            "description": "Link rate (Hz)",
            "type": "list",
            "options": [5, 10, 25, 40, 50]
        },
        "attenuation": {
            "command": "attenuation",
            "description": "Attenuation (dB)",
            "type": "range",
            "options": {"min": 0, "max": 30}
        },
        "address": {
            "command": "address",
            "description": "Module address",
            "type": "range",
            "options": {"min": 0, "max": 65534}
        },
        "pan": {
            "command": "pan",
            "description": "Network address",
            "type": "range",
            "options": {"min": 0, "max": 65534}
        },
        "bind": {
            "command": "bind",
            "description": "Binded address",
            "type": "range",
            "options": {"min": 0, "max": 65535}
        },
        "baudrate": {
            "command": "baudrate",
            "description": "Baudrate",
            "type": "list",
            "options": [57600, 100000, 115200, 400000, 420000]
        },
        "parity": {
            "command": "parity",
            "description": "Parity",
            "type": "list",
            "options": ["none", "even", "odd"]
        },
        "stopbits": {
            "command": "stopbits",
            "description": "Stop bits",
            "type": "list",
            "options": [1, 2]
        },
        "mode": {
            "command": "mode",
            "description": "Mode",
            "type": "list",
            "options": ["swarm+", "swarm", "longrange"]
        },
        "protocol": {
            "command": "protocol",
            "description": "Protocol",
            "type": "list",
            "options": ["crsf", "sbus", "mavlink", "raw"]
        },
        "timeslot": {
            "command": "timeslot",
            "description": "Time slotting",
            "type": "list",
            "options": [0, 1, 2]
        },
        "ttl": {
            "command": "ttl",
            "description": "Retransmissions (0=off, 1=on)",
            "type": "list",
            "options": [0, 1]
        },
        "ack": {
            "command": "ack",
            "description": "Acknowledge (0=off, 1=on)",
            "type": "list",
            "options": [0, 1]
        },
        "ewtests": {
            "command": "ewtests",
            "description": "EW tests (0=off, 1=on)",
            "type": "list",
            "options": [0, 1]
        },
        "trim": {
            "command": "trim",
            "description": "Crystal trim (calibration)",
            "type": "range",
            "options": {"min": 0, "max": 255}
        },
        "invert": {
            "command": "invert",
            "description": "Inversion (toggle)",
            "type": "toggle",
            "options": None
        }
    }

    @staticmethod
    def detect_modems() -> List[Dict]:
        """
        Этап 1: Обнаружение всех модемов на COM-портах

        Returns:
            List[Dict]: Список найденных модемов с параметрами
        """
        print("\n" + "=" * 60)
        print("   ОБНАРУЖЕНИЕ МОДЕМОВ")
        print("=" * 60)

        results = ModemScanner.scan_all_ports()
        ModemScanner.print_scan_results(results)

        modems = []
        for info in results:
            if info.port_type == PortType.MANAGEMENT:
                modem_data = {
                    "port": info.port,
                    "type": info.modem_type.value,
                    "version": info.version,
                    "sn": info.serial_number,
                    "config": info.config or {}
                }
                modems.append(modem_data)

        print(f"\n✅ Найдено модемов: {len(modems)}")
        return modems

    @staticmethod
    def show_parameters(config: Dict) -> None:
        """
        Показать нумерованный список параметров с текущими значениями
        """
        print("\n" + "-" * 60)
        print("   ТЕКУЩИЕ ПАРАМЕТРЫ")
        print("-" * 60)

        idx = 1
        for param_name, param_info in ModemEditor.PARAMETERS.items():
            current = config.get(param_name, "не установлен")
            options_str = ModemEditor._format_options(param_info)
            print(f"   {idx:2d}. {param_info['description']:30} = {current}  [{options_str}]")
            idx += 1

        print("\n   0. Назад")
        print("-" * 60)

    @staticmethod
    def _format_options(param_info: Dict) -> str:
        """Форматировать варианты для отображения"""
        if param_info["type"] == "list":
            return ", ".join(str(o) for o in param_info["options"])
        elif param_info["type"] == "range":
            return f"{param_info['options']['min']}-{param_info['options']['max']}"
        elif param_info["type"] == "toggle":
            return "toggle (on/off)"
        return ""

    @staticmethod
    def _format_options_for_selection(param_info: Dict) -> List[str]:
        """Форматировать варианты для выбора пользователем"""
        if param_info["type"] == "list":
            return [str(o) for o in param_info["options"]]
        elif param_info["type"] == "range":
            return [f"значение от {param_info['options']['min']} до {param_info['options']['max']}"]
        elif param_info["type"] == "toggle":
            return ["Изменить инверсию (toggle)"]
        return []

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
    def edit_modem(port: str, config: Dict) -> bool:
        """
        Этап 2: Редактирование параметров модема

        Args:
            port: COM-порт модема
            config: Текущая конфигурация

        Returns:
            bool: True если были изменения
        """
        controller = ModemController(port)

        try:
            controller.connect()
            print(f"\n✅ Подключено к {port}")

            changed = False

            while True:
                # Показываем параметры
                ModemEditor.show_parameters(config)

                # Выбор параметра
                max_idx = len(ModemEditor.PARAMETERS)
                choice = ModemEditor.get_user_choice(
                    f"\nВыберите параметр для изменения (1-{max_idx}, 0-выход): ",
                    max_idx
                )

                if choice == 0:
                    break

                # Получаем имя параметра
                param_names = list(ModemEditor.PARAMETERS.keys())
                param_name = param_names[choice - 1]
                param_info = ModemEditor.PARAMETERS[param_name]

                # Редактируем параметр
                new_value = ModemEditor._edit_parameter(
                    controller, param_name, param_info, config
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
            controller.disconnect()

    @staticmethod
    def _edit_parameter(
            controller: ModemController,
            param_name: str,
            param_info: Dict,
            config: Dict
    ) -> Optional[Any]:
        """
        Редактировать один параметр
        """
        current = config.get(param_name, "не установлен")
        command = param_info["command"]

        print(f"\n" + "=" * 50)
        print(f"   ИЗМЕНЕНИЕ: {param_info['description']}")
        print("=" * 50)
        print(f"   Текущее значение: {current}")
        print(f"   Команда: {command}")

        if param_info["type"] == "toggle":
            # Toggle: просто спрашиваем "Изменить?"
            print(f"   Тип: переключатель (toggle)")
            while True:
                choice = input("\n   Изменить инверсию? (y/n): ").strip().lower()
                if choice in ['y', 'yes', 'д', 'да']:
                    # Отправляем команду invert
                    success, response = controller.send_command("invert")
                    if success:
                        print("   ✅ Инверсия изменена")
                        # Обновляем состояние из print
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

        elif param_info["type"] == "list":
            # Список: показываем варианты
            options = param_info["options"]
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

            # Отправляем команду
            cmd = f"{command} {new_value}"
            print(f"\n   Отправка: {cmd}")
            success, response = controller.send_command(cmd)

            if success:
                print("   ✅ Команда выполнена")
                # Проверяем через print
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

        elif param_info["type"] == "range":
            # Диапазон: спрашиваем значение
            min_val = param_info["options"]["min"]
            max_val = param_info["options"]["max"]
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

            # Отправляем команду
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
            print(f"   ❌ Неизвестный тип параметра: {param_info['type']}")
            return None

    @staticmethod
    def run():
        """
        Запуск интерактивного редактора
        """
        print("\n" + "=" * 60)
        print("   ИНТЕРАКТИВНЫЙ РЕДАКТОР ПАРАМЕТРОВ")
        print("=" * 60)

        # Этап 1: Обнаружение модемов
        modems = ModemEditor.detect_modems()

        if not modems:
            print("\n❌ Модемы не найдены")
            return

        # Выбор модема для редактирования
        print("\n" + "-" * 60)
        print("   ВЫБОР МОДЕМА ДЛЯ РЕДАКТИРОВАНИЯ")
        print("-" * 60)

        for i, modem in enumerate(modems, 1):
            config = modem.get("config", {})
            print(
                f"   {i}. {modem['port']} ({modem['type']}) - freq={config.get('freq', '?')}, code={config.get('code', '?')}")

        print("\n   0. Выход")
        print("-" * 60)

        choice = ModemEditor.get_user_choice(
            f"\nВыберите модем (1-{len(modems)}, 0-выход): ",
            len(modems)
        )

        if choice == 0:
            print("\nВыход...")
            return

        selected = modems[choice - 1]
        port = selected["port"]
        config = selected.get("config", {})

        print(f"\n📌 Редактирование: {port} ({selected['type']})")

        # Этап 2: Редактирование
        changed = ModemEditor.edit_modem(port, config)

        if changed:
            print("\n✅ Параметры изменены")
        else:
            print("\nℹ️ Изменений не было")

        print("\n" + "=" * 60)
        print("   РАБОТА ЗАВЕРШЕНА")
        print("=" * 60)


if __name__ == "__main__":
    ModemEditor.run()