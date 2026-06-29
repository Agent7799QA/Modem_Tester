"""
Тестирование работы с профилями
"""

import sys

from core.modem.controller import ModemController
from cli.profiles import Profiles
from core.modem.exceptions import ModemConnectionError
from cli.read_modem import get_port_from_user, list_available_ports


def test_profiles(com_port: str):
    """Тестирование применения профилей к модему"""

    print(f"\n=== Тестирование профилей на порту {com_port} ===\n")

    controller = ModemController(com_port)

    try:
        print("1. Подключение...")
        controller.connect()
        print("   ✅ Подключено")

        print("\n2. Текущая конфигурация:")
        config = controller.get_config()

        if config:
            # Проверяем, является ли config DTO
            if hasattr(config, 'to_dict'):
                config_dict = config.to_dict()
                print(f"   Тип: DTO ({type(config).__name__})")
            else:
                config_dict = config
                print(f"   Тип: Dict")

            print(f"   Количество параметров: {len(config_dict)}")
            for key, value in config_dict.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ Не удалось получить конфигурацию")
            return

        print("\n3. Тестирование профилей:")

        profile_names = Profiles.list_names()
        print(f"   Найдено профилей: {len(profile_names)}")

        for name in profile_names:
            print(f"\n   📌 Профиль: {name}")
            profile = Profiles.get(name)
            if not profile:
                print("      ❌ Профиль не найден")
                continue

            # Выводим параметры профиля
            if hasattr(profile, 'to_dict'):
                params = profile.to_dict()
                print(f"      Параметры: {params}")

            # Применяем профиль
            results = controller.apply_config(profile)
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
            if hasattr(final, 'to_dict'):
                final_dict = final.to_dict()
            else:
                final_dict = final
            for key, value in final_dict.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ Не удалось получить конфигурацию")

    except ModemConnectionError as e:
        print(f"❌ Ошибка подключения: {e}")
        return 1
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        controller.disconnect()
        print("\n   ✅ Отключено")

    print("\n=== Тест завершен ===")
    return 0


def main():
    """Основная функция"""
    if len(sys.argv) >= 2:
        com_port = sys.argv[1]
        print(f"Использован порт из аргумента: {com_port}")
    else:
        ports = list_available_ports()
        if not ports:
            print("\n❌ COM-порты не найдены.")
            print("   Проверьте подключение модема и установку драйверов.")
            sys.exit(1)

        print("\nДоступные COM-порты:")
        for i, port in enumerate(ports, 1):
            print(f"  {i}. {port}")

        com_port = get_port_from_user()
        if not com_port:
            print("\n❌ Порт не выбран. Выход.")
            sys.exit(1)

    sys.exit(test_profiles(com_port))


if __name__ == "__main__":
    main()