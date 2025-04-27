import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_x_token():
    login_url = os.getenv("UXIM_LOGIN_URL")
    login = os.getenv("UXIM_LOGIN")
    password = os.getenv("UXIM_PASSWORD")

    payload = {
        "login": login,
        "password": password
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(login_url, json=payload, headers=headers)
        print(f"🔍 Статус: {response.status_code}")

        if response.status_code == 200:
            # Ищем X-TOKEN в заголовке Set-Cookie
            set_cookie = response.headers.get("Set-Cookie", "")
            print(f"🍪 Set-Cookie: {set_cookie}")
            for cookie in set_cookie.split(";"):
                if "X-TOKEN=" in cookie:
                    token = cookie.strip().split("X-TOKEN=")[-1]
                    print(f"✅ Получен X-TOKEN: {token[:30]}...")
                    return token
            print("❌ X-TOKEN не найден в заголовках ответа")
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
    
    return None
