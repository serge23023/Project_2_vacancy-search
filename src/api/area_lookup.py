import requests
import json
import os

AREA_FILE = "data/areas.json"


def load_areas() -> list:
    """
    Загружает справочник регионов из файла или по API.
    """
    if os.path.exists(AREA_FILE):
        with open(AREA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        response = requests.get("https://api.hh.ru/areas")
        response.raise_for_status()
        data = response.json()
        with open(AREA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    except requests.RequestException as e:
        print("Ошибка загрузки справочника регионов:", e)
        return []


def flatten_areas(areas: list) -> list[dict]:
    """
    Распаковывает вложенные регионы в плоский список.
    """
    flat = []

    def walk(area_list):
        for area in area_list:
            flat.append({"id": area["id"], "name": area["name"]})
            if area.get("areas"):
                walk(area["areas"])

    walk(areas)
    return flat


def suggest_areas_by_input(user_input: str) -> list[dict]:
    """
    Возвращает список подходящих регионов по части названия.
    """
    areas = flatten_areas(load_areas())
    query = user_input.strip().lower()
    return [a for a in areas if query in a["name"].lower()]


def get_area_id_from_user_input(user_input: str) -> str | None:
    """
    Спрашивает пользователя, если найдено несколько похожих регионов.
    """
    matches = suggest_areas_by_input(user_input)
    if not matches:
        print("Регион не найден.")
        return None
    elif len(matches) == 1:
        return matches[0]["id"]
    else:
        print("\nНайдено несколько регионов:")
        for i, area in enumerate(matches, 1):
            print(f"{i}. {area['name']}")
        try:
            index = int(input("Выберите номер региона: ")) - 1
            if 0 <= index < len(matches):
                return matches[index]["id"]
        except ValueError:
            pass
        print("Неверный выбор.")
        return None
