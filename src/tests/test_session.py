"""
Тестирование сессии с двумя модемами
"""

import time
from core.session import ModemSession
from core.modem.scanner import ModemScanner
from tests.profiles import Profiles
from core.modem.exceptions import ModemConnectionError


def test_session():
    """Тест сессии с двумя модемами"""
    print("\n" + "=" * 60)
    print("   ТЕСТ СЕССИИ: TX + RX МОДЕМЫ")
    print("=" * 60)

    # Сначала сканируем порты
    print("\n🔍 Сканирование портов...")
    results = ModemScanner.scan_all_ports()
    ModemScanner.print_scan_results(results)

    # Находим TX и RX
    found = ModemScanner.find_modems()

    if found.get("tx") and found.get("rx"):
        print(f"\n✅ Автоматически найдены:")
        print(f"   TX: {found['tx']}")
        print(f"   RX: {found['rx']}")
        session = ModemSession(tx_com=found['tx'], rx_com=found['rx'])
    else:
        print("\n⚠️ Не все порты найдены автоматически. Переход к ручному выбору...")
        session = ModemSession()  # вызовет ручной выбор

    if not session.tx_com or not session.rx_com:
        print("\n❌ Не удалось определить порты")
        return

    print(f"\n📌 Используемые порты:")
    print(f"   TX: {session.tx_com}")
    print(f"   RX: {session.rx_com}")

    try:
        # 1. Применяем профиль
        print("\n" + "-" * 60)
        config = Profiles.basic_3500()
        print("Применяем профиль: basic_3500")

        if not session.configure(config):
            print("❌ Не удалось применить конфигурацию")
            return

        # 2. Запускаем CRSF-поток
        print("\n" + "-" * 60)
        if not session.start_streaming():
            print("❌ Не удалось запустить CRSF-поток")
            return

        # 3. Собираем телеметрию
        print("\n" + "-" * 60)
        print("Сбор телеметрии (10 секунд)...")
        print("Нажмите Ctrl+C для остановки\n")

        try:
            for i in range(10):
                print(f"  [{i+1}/10] Сбор данных...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n   ⚠️ Прервано пользователем")

        # 4. Останавливаем поток
        print("\n" + "-" * 60)
        session.stop_streaming()

        print("\n" + "=" * 60)
        print("   ТЕСТ ЗАВЕРШЕН УСПЕШНО")
        print("=" * 60)

    except ModemConnectionError as e:
        print(f"\n❌ Ошибка подключения: {e}")
        session.stop_streaming()
    except KeyboardInterrupt:
        print("\n\n⚠️ Тест прерван пользователем")
        session.stop_streaming()


if __name__ == "__main__":
    test_session()