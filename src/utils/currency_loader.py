import requests
import json
import os

CURRENCY_FILE = "data/currencies.json"
DICTIONARIES_URL = "https://api.hh.ru/dictionaries"


def fetch_and_save_currency_rates():
    """
    Загружает справочник валют из hh.ru/dictionaries и сохраняет в currencies.json
    """
    try:
        response = requests.get(DICTIONARIES_URL)
        response.raise_for_status()
        data = response.json()

        currency_list = data.get("currency", [])

        # Фильтруем только нужные поля: code и rate
        cleaned = [
            {"code": entry["code"], "rate": entry["rate"]}
            for entry in currency_list
            if entry.get("rate")  # Только если rate задан
        ]

        os.makedirs("data", exist_ok=True)

        with open(CURRENCY_FILE, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        print("Курсы валют успешно обновлены и сохранены в data/currencies.json")

    except requests.RequestException as e:
        print(f"Ошибка при загрузке валют из /dictionaries: {e}")
