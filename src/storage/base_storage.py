from abc import ABC, abstractmethod
from typing import List
from src.models.vacancy import Vacancy


class Storage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        pass  # pragma: no cover

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass  # pragma: no cover
