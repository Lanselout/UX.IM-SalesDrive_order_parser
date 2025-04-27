import time
from datetime import datetime, timezone
from dotenv import load_dotenv

from auth import get_x_token
from fetch_from_uxim_api import fetch_orders_from_uxim
from mapper import map_order_for_salesdrive
from send_to_crm import send_to_crm
from update_ux_order import update_ux_order
from sync_tracker import get_last_sync_time, update_last_sync_time

load_dotenv()

SYNC_INTERVAL = 15 * 60  # 15 минут

def main():
    while True:
        print("🚀 Старт цикла синхронизации")

        try:
            token = get_x_token()
            if not token:
                print("❌ Ошибка авторизации. Повтор через 15 минут.")
                time.sleep(SYNC_INTERVAL)
                continue

            # Получаем заказы со статусом new
            orders = fetch_orders_from_uxim(token)

            if not orders:
                print("📭 Новых заказов нет.")
            else:
                for order in orders:
                    try:
                        mapped = map_order_for_salesdrive(order)
                        success = send_to_crm(mapped)

                        if success:
                            # После успешной отправки меняем статус
                            update_ux_order(order_id=order.get("id"), new_status="process", x_token=token)
                    except Exception as e:
                        print(f"❌ Ошибка обработки заказа #{order.get('id')}: {e}")

            # Обновляем last_sync на текущее время
            now_utc = datetime.now(timezone.utc)
            update_last_sync_time(now_utc)

        except KeyboardInterrupt:
            print("\n🛑 Скрипт остановлен пользователем.")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка цикла: {e}")

        print(f"⏳ Ждем {SYNC_INTERVAL // 60} минут до следующего запуска...\n")
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    main()
