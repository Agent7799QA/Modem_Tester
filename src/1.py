from core.modem.controller import ModemController

port = "COM12"

print(f"=== Тест RX на порту {port} ===\n")

ctrl = ModemController(port)

try:
    print("1. Подключение...")
    ctrl.connect()
    print("   ✅ Подключено")

    print("\n2. Отправка 'help'...")
    success, response = ctrl.send_command("help", timeout=1.0)
    if success:
        print("   ✅ help выполнен")
        lines = response.strip().split('\n')
        for line in lines[:5]:
            print(f"      {line}")
    else:
        print(f"   ❌ help не выполнен: {response[:100] if response else 'нет ответа'}")

    print("\n3. Отправка 'print'...")
    success, response = ctrl.send_command("print", timeout=1.0)
    if success:
        print("   ✅ print выполнен")
        lines = response.strip().split('\n')
        for line in lines[:5]:
            print(f"      {line}")
    else:
        print(f"   ❌ print не выполнен: {response[:100] if response else 'нет ответа'}")

    print("\n4. get_config()...")
    config = ctrl.get_config()
    if config:
        print("   ✅ Конфигурация получена")
        for key, value in config.items():
            print(f"      {key}: {value}")
    else:
        print("   ❌ Не удалось получить конфигурацию")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")

finally:
    ctrl.disconnect()
    print("\n✅ Отключено")
