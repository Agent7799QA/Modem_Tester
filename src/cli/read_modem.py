def list_available_ports():
    """Получить список доступных COM-портов"""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def get_port_from_user():
    """Запросить у пользователя номер COM-порта"""
    ports = list_available_ports()

    if not ports:
        print("\n❌ COM-порты не найдены.")
        return None

    while True:
        try:
            choice = input("\nВыберите номер порта (или 'q' для выхода): ").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                return ports[idx]
            else:
                print(f"❌ Неверный номер. Введите число от 1 до {len(ports)}")
        except ValueError:
            print("❌ Пожалуйста, введите число или 'q' для выхода")
        except KeyboardInterrupt:
            print("\n\nВыход...")
            return None