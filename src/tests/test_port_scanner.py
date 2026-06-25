"""
Тест сканера портов
"""

from core.modem.port_scanner import scan_ports, print_modems


def test_scanner():
    """Тест сканера портов"""
    print("\n" + "=" * 60)
    print("   ТЕСТ СКАНЕРА ПОРТОВ")
    print("=" * 60)

    modems = scan_ports()
    print_modems(modems)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_scanner()