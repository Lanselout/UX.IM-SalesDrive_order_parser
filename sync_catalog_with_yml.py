import time
import os
from dotenv import load_dotenv
from auth import get_x_token
from fetch_from_uxim_api import fetch_products_from_site
from fetch_from_yml import fetch_products_from_yml
from update_stock import update_stock
from update_price import update_price

load_dotenv()

YML_URL = os.getenv("YML_URL")
SYNC_INTERVAL = 24 * 60 * 60  # 24 часа в секундах

def sync_catalog():
    print("🚀 Запуск синхронизации каталога товаров...")

    x_token = get_x_token()
    if not x_token:
        print("❌ Не удалось получить X-TOKEN для UXIM.")
        return

    # Загружаем товары из YML и с сайта
    yml_products = fetch_products_from_yml(YML_URL)
    site_products = fetch_products_from_site(x_token)

    # Приводим статьи сайта к нормальному виду
    site_articles = {key.strip().upper(): value for key, value in site_products.items()}

    for sku, yml_data in yml_products.items():
        yml_id = sku.strip().upper()

        site_product = site_articles.get(yml_id)

        if not site_product:
            print(f"⚠️ Товар с ID {sku} не найден на сайте.")
            continue

        site_available = site_product.get("stock", True)
        site_price = float(site_product.get("price", 0))

        # Проверяем наличие
        if yml_data["available"] != site_available:
            print(f"🔄 Обновляем наличие для ID {sku}: {site_available} ➔ {yml_data['available']}")
            update_stock(
                item_id=site_product["id"],
                stock=yml_data["available"],
                x_token=x_token
            )

        # Проверяем цену
        if abs(yml_data["price"] - site_price) >= 0.01:
            print(f"💸 Обновляем цену для ID {sku}: {site_price} ➔ {yml_data['price']}")
            update_price(
                product_data=site_product,
                new_price=yml_data["price"],
                x_token=x_token
            )

    print("✅ Синхронизация каталога завершена.")

def main():
    while True:
        try:
            sync_catalog()
        except KeyboardInterrupt:
            print("\n🛑 Скрипт остановлен пользователем.")
            break
        except Exception as e:
            print(f"❌ Ошибка выполнения синхронизации: {e}")

        print(f"⏳ Ожидание {SYNC_INTERVAL // 3600} часов до следующего запуска...\n")
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    main()
