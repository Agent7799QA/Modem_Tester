"""
Тест проверки синхронизации модемов
"""

from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError
from core.verifier import ModemVerifier


def test_verify():
    """Тест проверки синхронизации"""
    print("\n" + "=" * 60)
    print("   ТЕСТ ПРОВЕРКИ СИНХРОНИЗАЦИИ")
    print("=" * 60)

    # Сканируем порты один раз
    print("\n🔍 Сканирование портов...")
    results = ModemScanner.scan_all_ports()
    ModemScanner.print_scan_results(results)

    # Находим TX и RX из результатов сканирования
    tx_port = None
    rx_port = None

    for info in results:
        if info.modem_type == ModemType.TX and info.port_type == PortType.MANAGEMENT:
            tx_port = info.port
        elif info.modem_type == ModemType.RX and info.port_type == PortType.MANAGEMENT:
            rx_port = info.port

    if not tx_port or not rx_port:
        print("\n❌ Не найдены оба модема (TX и RX)")
        print(f"   TX: {tx_port}")
        print(f"   RX: {rx_port}")
        return

    print(f"\n📌 Используемые порты:")
    print(f"   TX: {tx_port}")
    print(f"   RX: {rx_port}")

    tx_controller = ModemController(tx_port)
    rx_controller = ModemController(rx_port)

    try:
        # Проверяем синхронизацию
        success, result = ModemVerifier.verify(tx_controller, rx_controller)

        # Выводим отчёт
        ModemVerifier.print_verification_report(result)

    except ModemConnectionError as e:
        print(f"\n❌ Ошибка подключения: {e}")
    except KeyboardInterrupt:
        print("\n\n⚠️ Тест прерван пользователем")
    finally:
        tx_controller.disconnect()
        rx_controller.disconnect()


if __name__ == "__main__":
    test_verify()