import os
import requests
import json
from typing import Optional
from datetime import datetime

# Загружаем переменные окружения
ORDERS_API_URL = os.getenv("UXIM_API_URL")
PRODUCTS_API_URL = os.getenv("UXIM_PRODUCTS_URL")

def fetch_orders_from_uxim(x_token: str) -> list:
    """
    Получение заказов со статусом 'new' с сервера UXIM.
    """

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-TOKEN": x_token,
    }

    cookies = {
        "X-TOKEN": x_token
    }

    payload = {
        "filter": {
            "status": "new"
        }
    }

    try:
        response = requests.post(ORDERS_API_URL, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()

        data = response.json()

        orders = data.get("result", [])

        print(f"📦 Получено заказов со статусом NEW: {len(orders)}")
        return orders

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при получении заказов: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка декодирования JSON: {e}")
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")

    return []

def fetch_products_from_site(x_token: str) -> dict:
    """
    Загружает ВСЕ товары с сайта UXIM через POST-запрос с правильной структурой body (с фильтром).
    """

    API_PRODUCT_URL = "https://pitaka.admin.ux.im/api/item/filter"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-TOKEN": x_token,
    }

    cookies = {
        "X-TOKEN": x_token,
    }

    all_products = []
    page = 1
    per_page = 50  # Можно сразу 50 товаров на страницу

    while True:
        payload = {
            "filter": {
                "page": page,
                "perPage": per_page
            }
        }

        response = requests.post(API_PRODUCT_URL, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()

        data = response.json()

        products_list = data.get("list", []) or data.get("result", [])

        if not products_list:
            print(f"ℹ️ Нет товаров на странице {page}. Остановили загрузку.")
            break

        all_products.extend(products_list)
        print(f"📦 Загружено товаров на странице {page}: {len(products_list)}")

        if len(products_list) < per_page:
            break  # это последняя страница

        page += 1

    products_by_article = {}
    for item in all_products:
        article = item.get("article")
        if article:
            products_by_article[article.strip().upper()] = item

    print(f"✅ Загружено товаров всего: {len(products_by_article)}")
    return products_by_article
