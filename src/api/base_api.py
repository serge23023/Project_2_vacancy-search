from abc import ABC, abstractmethod
from typing import List, Dict


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получает список вакансий по ключевому слову.
        """
        pass  # pragma: no cover
