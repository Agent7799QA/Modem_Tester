"""
Тестирование работы с модемом
"""

import sys

import serial.tools.list_ports

from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError, ModemCommandError


def list_available_ports():
    """
    Получить список доступных COM-портов

    Returns:
        list: Список имен портов
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def get_port_from_user():
    """
    Запросить у пользователя номер COM-порта

    Returns:
        str: Имя выбранного порта или None
    """
    print("\n" + "=" * 50)
    print("   ПОИСК МОДЕМА САЛАНГАНА-К3")
    print("=" * 50)

    ports = list_available_ports()

    if not ports:
        print("\n❌ COM-порты не найдены.")
        print("   Проверьте подключение модема и установку драйверов.")
        return None

    print("\nДоступные COM-порты:")
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port}")

    print("\n" + "-" * 50)
    while True:
        try:
            choice = input("Выберите номер порта (или 'q' для выхода): ").strip()

            if choice.lower() == 'q':
                return None

            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                selected_port = ports[idx]
                print(f"\n✅ Выбран порт: {selected_port}")
                return selected_port
            else:
                print(f"❌ Неверный номер. Введите число от 1 до {len(ports)}")

        except ValueError:
            print("❌ Пожалуйста, введите число или 'q' для выхода")
        except KeyboardInterrupt:
            print("\n\nВыход...")
            return None


def ask_full_output() -> bool:
    """
    Спросить у пользователя, показывать полный или краткий вывод

    Returns:
        bool: True если полный вывод, False если краткий
    """
    print("\n" + "-" * 50)
    print("   ВЫБОР РЕЖИМА ВЫВОДА")
    print("-" * 50)
    print("   1. Краткий вывод (только начало)")
    print("   2. Полный вывод (все данные)")

    while True:
        try:
            choice = input("\nВыберите режим (1 или 2): ").strip()
            if choice == '1':
                return False
            elif choice == '2':
                return True
            else:
                print("   ❌ Введите 1 или 2")
        except KeyboardInterrupt:
            print("\n\nВыход...")
            return False


def print_response(response: str, full: bool, max_lines: int = 5):
    """
    Вывести ответ модема с учётом режима вывода

    Args:
        response: Ответ модема
        full: True — полный вывод, False — краткий
        max_lines: Максимальное строк для краткого вывода
    """
    if not response:
        print("   (пустой ответ)")
        return

    lines = response.strip().split('\n')

    if full:
        print(f"   Ответ ({len(lines)} строк):")
        for line in lines:
            print(f"      {line}")
    else:
        print(f"   Ответ ({len(lines)} строк):")
        for line in lines[:max_lines]:
            print(f"      {line}")
        if len(lines) > max_lines:
            print(f"      ... и еще {len(lines) - max_lines} строк")


def test_modem_connection(com_port: str, full_output: bool = False):
    """
    Тест подключения к модему

    Args:
        com_port: Имя COM-порта
        full_output: True — полный вывод, False — краткий
    """
    print(f"\n=== Тестирование модема на порту {com_port} ===\n")
    if full_output:
        print("   Режим: ПОЛНЫЙ ВЫВОД")
    else:
        print("   Режим: КРАТКИЙ ВЫВОД")

    controller = ModemController(com_port)

    try:
        # 1. Подключение
        print("1. Подключение к модему...")
        controller.connect()
        print(f"   ✅ Подключено к {com_port}")
        print(f"   Статус: {controller.is_connected()}")

        # 2. Проверка команды help
        print("\n2. Отправка команды 'help'...")
        success, response = controller.send_command("help")
        if success:
            print("   ✅ Команда выполнена")
            print_response(response, full_output)
        else:
            print("   ❌ Ошибка выполнения")
            print(f"   Ответ: {response[:100] if response else 'нет ответа'}")

        # 3. Получение конфигурации
        print("\n3. Получение текущей конфигурации...")
        config = controller.get_config()
        # Возвращает все 19 параметров:
        # protocol, freq, code, attenuation, address, pan, rate,
        # fhss, dsss, mode, type, baudrate, parity, stopbits,
        # timeslot, ttl, ack, trim, inverted
        if config:
            print("   ✅ Конфигурация получена")
            print(f"   Количество параметров: {len(config)}")
            for key, value in config.items():
                print(f"      {key}:\t {value}")
        else:
            print("   ❌ Не удалось получить конфигурацию")

        # 4. Отправка команды изменения частоты
        print("\n4. Изменение частоты на 3500 МГц...")
        success, response = controller.send_command("freq 3500")
        if success:
            print("   ✅ Частота изменена")
        else:
            print(f"   ❌ Ошибка: {response[:100] if response else 'нет ответа'}")

        # 5. Проверка изменений
        print("\n5. Проверка изменений...")
        config = controller.get_config()
        if config and config.get("freq") == 3500:
            print("   ✅ Частота успешно установлена на 3500 МГц")
        else:
            print("   ❌ Частота не изменилась")
            if config:
                print(f"      Текущая частота: {config.get('freq', 'неизвестно')}")

        # 6. Применение конфигурации через словарь
        print("\n6. Применение конфигурации через словарь...")
        test_config = {
            "freq": 4000,
            "fhss": 0,
            "dsss": 0,
            "code": 11,
            "rate": 50
        }
        results = controller.apply_config(test_config)
        all_ok = all(success for success, _ in results.values() if isinstance(success, bool))

        if all_ok:
            print("   ✅ Все команды выполнены успешно")
            for cmd, (success, response) in results.items():
                status = "✅" if success else "❌"
                resp_preview = response[:50] if response else "OK"
                print(f"      {status} {cmd}: {resp_preview}")
        else:
            print("   ❌ Некоторые команды не выполнены")
            for cmd, (success, response) in results.items():
                status = "✅" if success else "❌"
                resp_preview = response[:50] if response else "нет ответа"
                print(f"      {status} {cmd}: {resp_preview}")

    except ModemConnectionError as e:
        print(f"\n❌ Ошибка подключения: {e}")
        return 1

    except ModemCommandError as e:
        print(f"\n❌ Ошибка команды: {e}")
        return 1

    except KeyboardInterrupt:
        print("\n\n⚠️ Тест прерван пользователем")
        return 0

    finally:
        print("\n7. Отключение от модема...")
        controller.disconnect()
        print("   ✅ Отключено")

    print("\n" + "=" * 50)
    print("   ТЕСТ ЗАВЕРШЕН УСПЕШНО")
    print("=" * 50)
    return 0


def main():
    """Основная функция"""

    # Проверяем аргументы командной строки
    if len(sys.argv) >= 2:
        com_port = sys.argv[1]
        print(f"Использован порт из аргумента: {com_port}")
    else:
        com_port = get_port_from_user()
        if not com_port:
            print("\n❌ Порт не выбран. Выход.")
            sys.exit(1)

    # Спрашиваем режим вывода (если не передан аргумент)
    if len(sys.argv) >= 3 and sys.argv[2].lower() in ['full', '--full', '-f']:
        full_output = True
        print("   Режим: ПОЛНЫЙ ВЫВОД (из аргумента)")
    else:
        full_output = ask_full_output()

    sys.exit(test_modem_connection(com_port, full_output))


if __name__ == "__main__":
    main()
