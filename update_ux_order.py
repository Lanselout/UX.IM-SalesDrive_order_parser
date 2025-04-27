import os
import requests

UPDATE_URL = os.getenv("UXIM_UPDATE_URL")

def update_ux_order(order_id: int, new_status: str, x_token: str):
    """
    Обновляет статус заказа в UXIM.
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
        "id": order_id,
        "status": new_status
    }

    try:
        response = requests.put(UPDATE_URL, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()

        print(f"✅ Статус заказа #{order_id} успешно обновлен на {new_status}")

    except Exception as e:
        print(f"❌ Ошибка при обновлении статуса заказа #{order_id}: {e}")
