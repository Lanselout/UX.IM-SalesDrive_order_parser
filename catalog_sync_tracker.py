# catalog_sync_tracker.py

import json
import os
from datetime import datetime, timezone, timedelta

CATALOG_SYNC_FILE = "last_catalog_sync.json"

def read_last_catalog_sync_time():
    """
    Считывает время последней синхронизации каталога из файла.
    Если файл отсутствует или повреждён — возвращает None.
    """
    if not os.path.exists(CATALOG_SYNC_FILE):
        return None

    try:
        with open(CATALOG_SYNC_FILE, "r") as file:
            data = json.load(file)
            last_sync_time = data.get("last_sync")
            if last_sync_time:
                return datetime.fromisoformat(last_sync_time)
    except (json.JSONDecodeError, KeyError, ValueError):
        print("⚠️ Ошибка при чтении времени последней синхронизации каталога.")
    return None

def write_catalog_sync_time(sync_time):
    """
    Записывает текущее время синхронизации каталога в файл.
    """
    with open(CATALOG_SYNC_FILE, "w") as file:
        json.dump({"last_sync": sync_time.isoformat()}, file, ensure_ascii=False, indent=2)
