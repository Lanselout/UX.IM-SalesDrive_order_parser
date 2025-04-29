import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from auth import get_x_token
from fetch_from_uxim_api import fetch_orders_from_uxim
from mapper import map_order_for_salesdrive
from send_to_crm import send_to_crm
from update_ux_order import update_ux_order
from sync_tracker import get_last_sync_time, update_last_sync_time
from sync_catalog_with_yml import sync_catalog
from catalog_sync_tracker import read_last_catalog_sync_time, write_catalog_sync_time

load_dotenv()

SYNC_INTERVAL = 15 * 60  # 15 минут
CATALOG_SYNC_INTERVAL_HOURS = 1  # раз в 1 час

def main():
    while True:
        print("🚀 Старт цикла синхронизации")

        try:
            token = get_x_token()
            if not token:
                print("❌ Ошибка авторизации. Повтор через 15 минут.")
                time.sleep(SYNC_INTERVAL)
                continue

            now_utc = datetime.now(timezone.utc)

            # 🔄 Проверяем необходимость синхронизации каталога
            last_catalog_sync = read_last_catalog_sync_time()
            if not last_catalog_sync or (now_utc - last_catalog_sync >= timedelta(hours=CATALOG_SYNC_INTERVAL_HOURS)):
                print("🔄 Пора синхронизировать каталог товаров с YML...")
                try:
                    sync_catalog()
                    write_catalog_sync_time(now_utc)
                    print(f"✅ Каталог успешно синхронизирован в {now_utc.isoformat()}")
                except Exception as e:
                    print(f"❌ Ошибка при синхронизации каталога: {e}")

            # 📦 Получаем заказы со статусом NEW
            orders = fetch_orders_from_uxim(token)

            if not orders:
                print("📭 Новых заказов нет.")
            else:
                for order in orders:
                    try:
                        mapped = map_order_for_salesdrive(order)
                        success = send_to_crm(mapped)

                        if success:
                            update_ux_order(order_id=order.get("id"), new_status="process", x_token=token)
                            print(f"✅ Заказ #{order.get('id')} успешно отправлен в CRM и обновлён в UXIM")
                        else:
                            print(f"⚠️ Ошибка отправки заказа #{order.get('id')} в CRM")
                    except Exception as e:
                        print(f"❌ Ошибка обработки заказа #{order.get('id')}: {e}")
                        print(f"⚠️ Пропускаем заказ: {order}")

            # 📝 Обновляем last_sync по заказам
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
