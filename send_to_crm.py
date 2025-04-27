import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
CRM_API_KEY = os.getenv("CRM_API_KEY", "").strip()

def send_to_crm(data: dict) -> bool:
    """
    Отправка заявки в CRM SalesDrive.
    """

    try:
        url = "https://smobile.salesdrive.me/handler/"
        headers = {
            "Content-Type": "application/json"
        }

        if "form" not in data or not data["form"]:
            data["form"] = CRM_API_KEY

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("✅ Заказ успешно отправлен в CRM")
            return True
        else:
            print(f"❌ Ошибка при отправке в CRM: {response.status_code} – {response.text}")
            return False

    except Exception as e:
        print(f"❌ Сетевая ошибка при отправке в CRM: {e}")
        return False
