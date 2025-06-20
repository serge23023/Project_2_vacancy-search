import requests
from typing import List, Dict
from src.api.base_api import JobAPI


class HeadHunterAPI(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(
        self,
        keyword: str,
        experience: str = None,
        salary: int = None,
        only_with_salary: bool = False,
        area: str = None,
    ) -> List[Dict]:

        params = {
            "text": keyword,
            "per_page": 20
        }

        if experience:
            params["experience"] = experience

        if salary:
            params["salary"] = salary

        if only_with_salary:
            params["only_with_salary"] = "True"

        if area:
            params["area"] = area

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.RequestException as e:
            print("Ошибка при подключении к hh.ru:", e)
            return []
