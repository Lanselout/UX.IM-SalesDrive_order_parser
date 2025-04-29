import os
import requests

def update_price(product_data: dict, new_price: float, x_token: str) -> bool:
    """
    Обновляет цену товара без потери других данных (фото, описания, наличия).
    Отправляет ПОЛНЫЙ объект товара обратно на сайт UXIM.
    """

    API_PRODUCT_URL = "https://pitaka.admin.ux.im/api/item"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-TOKEN": x_token,
    }

    cookies = {
        "X-TOKEN": x_token,
    }

    # Меняем только цену
    updated_product = product_data.copy()
    updated_product["price"] = new_price

    try:
        response = requests.put(API_PRODUCT_URL, headers=headers, cookies=cookies, json=updated_product)
        response.raise_for_status()

        print(f"✅ Цена товара ID {product_data.get('id')} успешно обновлена на {new_price} грн")
        return True

    except Exception as e:
        print(f"❌ Ошибка при обновлении цены товара ID {product_data.get('id')}: {e}")
        return False
