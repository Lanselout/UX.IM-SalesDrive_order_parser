import os
import requests

def update_stock(item_id: int, stock: bool, x_token: str) -> bool:
    """
    Обновляет только наличие товара на сайте UXIM.
    """

    url = f"https://pitaka.admin.ux.im/api/item"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-TOKEN": x_token,
    }

    cookies = {
        "X-TOKEN": x_token,
    }

    payload = {
        "id": item_id,
        "stock": stock
    }

    try:
        response = requests.put(url, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()

        print(f"✅ Наличие товара ID {item_id} обновлено на: {'В наличии' if stock else 'Нет в наличии'}")
        return True

    except Exception as e:
        print(f"❌ Ошибка обновления наличия товара ID {item_id}: {e}")
        return False
