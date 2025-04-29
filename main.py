# main.py

import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from auth import get_x_token
from fetch_from_uxim_api import fetch_orders_from_uxim
from mapper import map_order_for_salesdrive
from send_to_crm import send_to_crm
from update_ux_order import update_ux_order
from catalog_sync_tracker import read_last_catalog_sync_time, write_catalog_sync_time
from sync_catalog_with_yml import sync_catalog

# Загрузка переменных окружения
load_dotenv()

# Константы интервалов
ORDER_SYNC_INTERVAL_SECONDS = 15 * 60   # 15 минут в секундах
CATALOG_SYNC_INTERVAL_HOURS = 1         # 24 часа

def main():
    print("🚀 Старт основного воркера синхронизации заказов и каталога...")

    last_catalog_sync = read_last_catalog_sync_time()

    while True:
        now = datetime.now(timezone.utc)

        # Проверка необходимости синхронизации каталога
        if (last_catalog_sync is None) or (now - last_catalog_sync >= timedelta(hours=CATALOG_SYNC_INTERVAL_HOURS)):
            print("🔄 Пора синхронизировать каталог товаров с YML...")
            try:
                sync_catalog()
                write_catalog_sync_time(now)
                print(f"✅ Каталог успешно синхронизирован в {now.isoformat()}")
            except Exception as e:
                print(f"❌ Ошибка при синхронизации каталога: {e}")

        # Синхронизация заказов
        try:
            x_token = get_x_token()
            if not x_token:
                print("❌ Не удалось получить X-TOKEN. Пропускаем цикл...")
                time.sleep(ORDER_SYNC_INTERVAL_SECONDS)
                continue

            orders = fetch_orders_from_uxim(x_token)

            if not orders:
                print("📭 Новых заказов нет.")
            else:
                for order in orders:
                    order_id = order.get("id")
                    print(f"🔄 Обработка заказа #{order_id}")

                    mapped_order = map_order_for_salesdrive(order)
                    success = send_to_crm(mapped_order)

                    if success:
                        update_ux_order(order_id, "processing", x_token)
                        print(f"✅ Заказ #{order_id} успешно отправлен в CRM и обновлён на сайте UXIM.")
                    else:
                        print(f"❌ Ошибка отправки заказа #{order_id} в CRM.")

        except Exception as e:
            print(f"❌ Ошибка обработки заказов: {e}")

        print(f"⏳ Ожидание {ORDER_SYNC_INTERVAL_SECONDS // 60} минут до следующей проверки заказов...\n")
        time.sleep(ORDER_SYNC_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
