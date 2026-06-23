"""
Тестирование работы с модемом
"""

import sys
import time
import serial.tools.list_ports
from modem.controller import ModemController
from modem.exceptions import ModemConnectionError, ModemCommandError


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
    print("\n" + "="*50)
    print("   ПОИСК МОДЕМА САЛАНГАНА-К3")
    print("="*50)

    # Получаем список доступных портов
    ports = list_available_ports()

    if not ports:
        print("\n❌ COM-порты не найдены.")
        print("   Проверьте подключение модема и установку драйверов.")
        return None

    # Показываем список портов
    print("\nДоступные COM-порты:")
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port}")

    # Запрашиваем выбор
    print("\n" + "-"*50)
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


def test_modem_connection(com_port: str):
    """
    Тест подключения к модему

    Args:
        com_port: Имя COM-порта
    """
    print(f"\n=== Тестирование модема на порту {com_port} ===\n")

    # Создаем контроллер
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
            # Показываем первые строки ответа
            lines = response.strip().split('\n')
            print(f"   Ответ ({len(lines)} строк):")
            for line in lines[:5]:  # Показываем первые 5 строк
                print(f"      {line}")
            if len(lines) > 5:
                print(f"      ... и еще {len(lines) - 5} строк")
        else:
            print("   ❌ Ошибка выполнения")
            print(f"   Ответ: {response[:100] if response else 'нет ответа'}")

        # 3. Получение конфигурации
        print("\n3. Получение текущей конфигурации...")
        config = controller.get_config()
        if config:
            print("   ✅ Конфигурация получена")
            for key, value in config.items():
                print(f"      {key}: {value}")
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
        # Отключение
        print("\n7. Отключение от модема...")
        controller.disconnect()
        print("   ✅ Отключено")

    print("\n" + "="*50)
    print("   ТЕСТ ЗАВЕРШЕН УСПЕШНО")
    print("="*50)
    return 0


def main():
    """Основная функция"""

    # Проверяем аргументы командной строки
    if len(sys.argv) >= 2:
        com_port = sys.argv[1]
        print(f"Использован порт из аргумента: {com_port}")
    else:
        # Запрашиваем порт у пользователя
        com_port = get_port_from_user()

        if not com_port:
            print("\n❌ Порт не выбран. Выход.")
            sys.exit(1)

    # Запускаем тест
    sys.exit(test_modem_connection(com_port))


if __name__ == "__main__":
    main()