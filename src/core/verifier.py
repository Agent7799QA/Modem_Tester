"""
Проверка синхронизации модемов
Использует только управляющие порты (115200)
"""

from typing import Dict, Tuple

from core.modem.controller import ModemController
from core.modem.exceptions import ModemConnectionError


class ModemVerifier:
    """
    Проверка синхронизации модемов через управляющие порты
    """

    # Параметры, которые должны совпадать у TX и RX
    SYNC_PARAMS = ["freq", "code", "fhss", "dsss", "rate", "pan", "protocol"]

    @staticmethod
    def verify(
            tx_controller: ModemController,
            rx_controller: ModemController
    ) -> Tuple[bool, Dict]:
        """
        Проверить синхронизацию между TX и RX
        """
        print("\n🔍 Проверка синхронизации...")

        result = {
            "success": False,
            "tx_config": {},
            "rx_config": {},
            "checks": {},
            "errors": [],
            "warnings": []
        }

        try:
            # 1. Получаем конфигурацию с TX
            print("   Чтение конфигурации с TX...")
            tx_controller.connect()
            tx_info = tx_controller.get_config()

            # Проверяем сразу после получения, до disconnect
            if not tx_info:
                result["errors"].append("Не удалось получить конфигурацию TX")
                print("   ❌ Не удалось получить конфигурацию TX")
                tx_controller.disconnect()
                return False, result

            tx_controller.disconnect()
            result["tx_config"] = tx_info

            # 2. Получаем конфигурацию с RX
            print("   Чтение конфигурации с RX...")
            rx_controller.connect()
            rx_info = rx_controller.get_config()

            # Проверяем сразу после получения, до disconnect
            if not rx_info:
                result["errors"].append("Не удалось получить конфигурацию RX")
                print("   ❌ Не удалось получить конфигурацию RX")
                rx_controller.disconnect()
                return False, result

            rx_controller.disconnect()
            result["rx_config"] = rx_info

            # 3. Проверяем параметры
            print("\n   Проверка параметров:")
            all_match = True

            for param in ModemVerifier.SYNC_PARAMS:
                tx_val = tx_info.get(param)
                rx_val = rx_info.get(param)
                match = tx_val == rx_val

                result["checks"][param] = {
                    "tx": tx_val,
                    "rx": rx_val,
                    "match": match
                }

                status = "✅" if match else "❌"
                print(f"      {status} {param}: TX={tx_val}, RX={rx_val}")

                if not match:
                    all_match = False
                    result["errors"].append(
                        f"{param}: TX={tx_val}, RX={rx_val} (не совпадает)"
                    )

            # 4. Проверяем bind
            tx_addr = tx_info.get("address")
            rx_bind = rx_info.get("bind")

            if tx_addr is not None and rx_bind is not None:
                bind_match = tx_addr == rx_bind
                result["checks"]["bind"] = {
                    "tx_address": tx_addr,
                    "rx_bind": rx_bind,
                    "match": bind_match
                }

                status = "✅" if bind_match else "❌"
                print(f"      {status} bind: TX.address={tx_addr}, RX.bind={rx_bind}")

                if not bind_match:
                    all_match = False
                    result["errors"].append(
                        f"bind: TX.address={tx_addr}, RX.bind={rx_bind} (не совпадает)"
                    )

            result["success"] = all_match

            if all_match:
                print("\n   ✅ Модемы синхронизированы")
            else:
                print("\n   ❌ Модемы НЕ синхронизированы")
                for err in result["errors"]:
                    print(f"      - {err}")

            return all_match, result

        except ModemConnectionError as e:
            result["errors"].append(f"Ошибка подключения: {e}")
            print(f"   ❌ Ошибка подключения: {e}")
            return False, result

        except Exception as e:
            result["errors"].append(f"Неизвестная ошибка: {e}")
            print(f"   ❌ Ошибка: {e}")
            return False, result

    @staticmethod
    def print_verification_report(result: Dict) -> None:
        """
        Красиво вывести отчёт о проверке
        """
        print("\n" + "=" * 60)
        print("   ОТЧЁТ О ПРОВЕРКЕ СИНХРОНИЗАЦИИ")
        print("=" * 60)

        if result.get("success"):
            print("\n   ✅ СИНХРОНИЗАЦИЯ ПОДТВЕРЖДЕНА")
        else:
            print("\n   ❌ СИНХРОНИЗАЦИЯ НЕ ПОДТВЕРЖДЕНА")

        if result.get("errors"):
            print("\n   Ошибки:")
            for err in result["errors"]:
                print(f"      - {err}")

        if result.get("warnings"):
            print("\n   Предупреждения:")
            for warn in result["warnings"]:
                print(f"      - {warn}")

        print("\n" + "=" * 60)
