import json
import os
from typing import List
from src.models.vacancy import Vacancy
from src.storage.base_storage import Storage


class JSONStorage(Storage):
    def __init__(self, filename: str = "data/vacancies.json"):
        self._filename = filename
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        all_vacancies = self.get_vacancies()
        if vacancy.to_dict() not in [v.to_dict() for v in all_vacancies]:
            all_vacancies.append(vacancy)
            self._save(all_vacancies)

    def get_vacancies(self) -> List[Vacancy]:
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
            return [Vacancy.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Ошибка чтения JSON: {e}. Возвращаю пустой список.")
            return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        filtered = [v for v in vacancies if v.to_dict() != vacancy.to_dict()]
        self._save(filtered)

    def _save(self, vacancies: List[Vacancy]) -> None:
        with open(self._filename, "w") as f:
            json.dump([v.to_dict() for v in vacancies], f, indent=2)
