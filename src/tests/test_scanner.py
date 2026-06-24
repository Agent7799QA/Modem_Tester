"""
Тестирование сканера портов модема
"""

import sys
from core.modem.scanner import ModemScanner


def test_scanner():
    """Тест сканера портов"""
    print("\n" + "=" * 60)
    print("   ТЕСТ СКАНЕРА ПОРТОВ МОДЕМА")
    print("=" * 60)

    # Сканируем все порты
    results = ModemScanner.scan_all_ports()

    # Выводим результаты
    ModemScanner.print_scan_results(results)

    # Находим TX и RX
    found = ModemScanner.find_modems()

    print("\n" + "=" * 60)
    print("   АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ")
    print("=" * 60)
    print(f"\n   TX: {found.get('tx') or '❌ не найден'}")
    print(f"   RX: {found.get('rx') or '❌ не найден'}")

    if found.get("tx") and found.get("rx"):
        print("\n   ✅ Оба модема найдены автоматически!")
    else:
        print("\n   ⚠️ Не все модемы найдены. Проверьте подключение.")

    print("\n" + "=" * 60)
    print("   ТЕСТ ЗАВЕРШЕН")
    print("=" * 60)


if __name__ == "__main__":
    test_scanner()