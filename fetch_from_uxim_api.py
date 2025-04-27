import os
import requests
import json
from typing import Optional
from datetime import datetime

# Загружаем переменные окружения
API_URL = os.getenv("UXIM_API_URL")

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

    # Тело запроса с фильтром по статусу
    payload = {
        "filter": {
            "status": "new"
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, cookies=cookies, json=payload)
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
