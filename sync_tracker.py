from datetime import datetime, timezone
from dateutil.parser import isoparse
import json
import os

LAST_SYNC_FILE = "last_sync.json"


def get_last_sync_time() -> datetime:
    try:
        with open(LAST_SYNC_FILE, "r") as f:
            data = json.load(f)
            raw_time = data.get("last_sync_time")
            print(f"📄 Считанное значение времени: {raw_time} ({type(raw_time)})")
            return datetime.fromisoformat(raw_time)
    except Exception as e:
        now = datetime.now(timezone.utc)
        print(f"⚠️ Ошибка при чтении файла синхронизации: {e}")
        print(f"📁 Создан новый файл синхронизации с текущим временем (UTC): {now.isoformat()}")
        update_last_sync_time(now)
        return now


    try:
        with open(LAST_SYNC_FILE, "r") as f:
            data = json.load(f)
            last_sync_raw = data.get("last_sync")

            print(f"📄 Считанное значение времени: {last_sync_raw} ({type(last_sync_raw)})")

            if not last_sync_raw or not isinstance(last_sync_raw, str):
                raise ValueError("Поле 'last_sync' отсутствует или имеет некорректный формат")

            return isoparse(last_sync_raw)
    except Exception as e:
        print(f"⚠️ Ошибка при преобразовании времени: {e}. Используется текущее UTC-время.")
        now = datetime.now(timezone.utc)
        with open(LAST_SYNC_FILE, "w") as f:
            json.dump({"last_sync": now.isoformat()}, f)
        return now




def update_last_sync_time(new_time):
    if new_time.tzinfo is None:
        new_time = new_time.replace(tzinfo=timezone.utc)

    with open(LAST_SYNC_FILE, "w") as f:
        json.dump({"last_sync": new_time.isoformat()}, f)
    print(f"📝 Время последней синхронизации обновлено: {new_time.isoformat()}")
