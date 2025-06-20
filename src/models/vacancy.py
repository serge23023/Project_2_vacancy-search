class Vacancy:

    __slots__ = ("_title", "_link", "_salary_from", "_salary_to", "_currency", "_experience", "_area", "_employment")

    def __init__(self, title: str, link: str, salary: int | dict, experience: str, area: str, employment: str):
        self._title = title
        self._link = link
        self._salary_from, self._salary_to, self._currency = self._parse_salary(salary)
        self._experience = experience
        self._area = area
        self._employment = employment

    @staticmethod
    def _parse_salary(salary_data: int | dict) -> tuple[int, int, str]:
        if isinstance(salary_data, int):
            return salary_data, 0, "RUR"
        if isinstance(salary_data, dict):
            salary_from = salary_data.get("from") or 0
            salary_to = salary_data.get("to") or 0
            currency = salary_data.get("currency") or "RUR"
            return salary_from, salary_to, currency
        return 0, 0, "RUR"

    @property
    def title(self): return self._title

    @property
    def link(self): return self._link

    @property
    def salary_from(self): return self._salary_from

    @property
    def salary_to(self): return self._salary_to

    @property
    def salary(self): return self._salary_from or self._salary_to

    @property
    def currency(self): return self._currency

    @property
    def experience(self): return self._experience

    @property
    def area(self): return self._area

    @property
    def employment(self): return self._employment

    def __str__(self):
        from src.utils.helpers import convert_to_rub

        code = self.currency.upper()
        display_currency = "RUB" if code == "RUR" else code

        # salary range
        if self.salary_from and self.salary_to:
            salary_text = f"{self.salary_from} – {self.salary_to} {display_currency}"
        elif self.salary_from:
            salary_text = f"от {self.salary_from} {display_currency}"
        elif self.salary_to:
            salary_text = f"до {self.salary_to} {display_currency}"
        else:
            salary_text = "зарплата не указана"

        if (self.salary_from or self.salary_to) and code != "RUR":
            rub_from = convert_to_rub(self.salary_from, code) if self.salary_from else None
            rub_to = convert_to_rub(self.salary_to, code) if self.salary_to else None
            if rub_from and rub_to:
                salary_text += f" (~{rub_from} – {rub_to} руб.)"
            elif rub_from:
                salary_text += f" (~{rub_from} руб.)"
            elif rub_to:
                salary_text += f" (~{rub_to} руб.)"

        return (f"{self.title} | {salary_text} | {self.link} | "
                f"Регион: {self.area} | Опыт: {self.experience} | Занятость: {self.employment}")

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "experience": self.experience,
            "area": self.area,
            "employment": self.employment
        }

    @classmethod
    def from_dict(cls, data: dict):
        salary_data = {
            "from": data.get("salary_from", 0),
            "to": data.get("salary_to", 0),
            "currency": data.get("currency", "RUR")
        }
        return cls(
            title=data["title"],
            link=data["link"],
            salary=salary_data,
            experience=data.get("experience", "Не указано"),
            area=data.get("area", "Не указано"),
            employment=data.get("employment", "Не указано")
        )
