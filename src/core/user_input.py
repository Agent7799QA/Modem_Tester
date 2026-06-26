"""
Тестирование работы с профилями
"""

import sys
from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError
from core.user_input import get_port_from_user
from core.tests.profiles import Profiles


def test_profiles(com_port: str):
    """
    Тестирование применения профилей к модему

    Args:
        com_port: Имя COM-порта
    """
    print(f"\n=== Тестирование профилей на порту {com_port} ===\n")

    controller = ModemController(com_port)

    try:
        print("1. Подключение...")
        controller.connect()
        print("   ✅ Подключено")

        print("\n2. Текущая конфигурация:")
        current = controller.get_config()
        if current:
            for key, value in current.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ Не удалось получить конфигурацию")
            return

        print("\n3. Тестирование профилей:")

        for name in Profiles.list_names():
            print(f"\n   📌 Профиль: {name}")
            profile = Profiles.get(name)
            if not profile:
                print("      ❌ Профиль не найден")
                continue

            config_dict = profile.to_dict()
            print(f"      Параметры: {config_dict}")

            results = controller.apply_config(config_dict)
            all_ok = all(success for success, _ in results.values()
                         if isinstance(success, bool))

            if all_ok:
                print(f"      ✅ Профиль {name} применен")
            else:
                print(f"      ❌ Ошибка применения {name}")
                for cmd, (success, response) in results.items():
                    if not success and cmd != "connection_check":
                        print(f"         ❌ {cmd}: {response[:50] if response else 'нет ответа'}")

        print("\n4. Итоговая конфигурация:")
        final = controller.get_config()
        if final:
            for key, value in final.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ Не удалось получить конфигурацию")

    except ModemConnectionError as e:
        print(f"❌ Ошибка подключения: {e}")
        return 1
    finally:
        controller.disconnect()
        print("\n   ✅ Отключено")

    print("\n=== Тест завершен ===")
    return 0


def main():
    if len(sys.argv) >= 2:
        com_port = sys.argv[1]
    else:
        com_port = get_port_from_user("ВЫБОР ПОРТА ДЛЯ ТЕСТА ПРОФИЛЕЙ")
        if not com_port:
            print("Порт не выбран. Выход.")
            sys.exit(1)

    sys.exit(test_profiles(com_port))


if __name__ == "__main__":
    main()