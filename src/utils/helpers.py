import json
import os

from src.models.vacancy import Vacancy
import re


def to_vacancy_objects(data_list: list) -> list[Vacancy]:
    vacancies = []
    for item in data_list:
        vacancy = Vacancy(
            title=item.get("name", ""),
            link=item.get("alternate_url", ""),
            salary=item.get("salary", {}),
            experience=item.get("experience", {}).get("name", "Не указано"),
            area=item.get("area", {}).get("name", "Не указано"),
            employment=item.get("employment", {}).get("name", "Не указано")
        )
        if vacancy.salary > 0:
            vacancies.append(vacancy)
    return vacancies


def filter_by_keywords(vacancies: list, keywords: list[str]) -> list:
    return [
        v for v in vacancies
        if any(kw.lower() in (v.title + v.experience + v.area + v.employment).lower() for kw in keywords)
    ]


def filter_by_experience(vacancies: list, min_years: int) -> list:
    def has_required_exp(vac):
        years = re.findall(r"\d+", vac.experience)
        return any(int(y) >= min_years for y in years)
    return list(filter(has_required_exp, vacancies))


def filter_by_region(vacancies: list, region: str) -> list:
    return [v for v in vacancies if region.lower() in v.area.lower()]


def filter_by_employment(vacancies: list, employment: str) -> list:
    return [v for v in vacancies if employment.lower() in v.employment.lower()]


def filter_by_salary(vacancies: list, salary_input: str) -> list:
    salary_input = salary_input.replace(" ", "")
    if "-" not in salary_input:
        print("Неверный формат диапазона (ожидается от-до).")
        return vacancies
    try:
        min_sal, max_sal = map(int, salary_input.split("-"))
    except ValueError:
        print("Зарплата должна быть числом.")
        return vacancies

    return [
        v for v in vacancies
        if min_sal <= convert_to_rub(v.salary, v.currency) <= max_sal
    ]


def apply_user_filters(vacancies: list) -> None:
    filtered = vacancies

    keywords_input = input("Ключевые слова (через пробел, ENTER чтобы пропустить): ").strip()
    if keywords_input:
        keywords = keywords_input.split()
        filtered = filter_by_keywords(filtered, keywords)

    salary_input = input("Введите диапазон зарплат (например 80000-150000), ENTER чтобы пропустить: ").strip()
    if salary_input:
        filtered = filter_by_salary(filtered, salary_input)

    exp_input = input("Минимальный опыт в годах (например 2), ENTER чтобы пропустить: ").strip()
    if exp_input.isdigit():
        filtered = filter_by_experience(filtered, int(exp_input))

    region_input = input("Регион (например Москва), ENTER чтобы пропустить: ").strip()
    if region_input:
        filtered = filter_by_region(filtered, region_input)

    emp_input = input("Тип занятости (например Полная), ENTER чтобы пропустить: ").strip()
    if emp_input:
        filtered = filter_by_employment(filtered, emp_input)

    if filtered:
        try:
            n = int(input("Сколько показать топ-вакансий?: "))
        except ValueError:
            n = 5
        top = get_top_n(filtered, n)
        print(f"\nНайдено вакансий: {len(filtered)}\n")
        print("\nТоп вакансий:")
        for v in top:
            print(v)
    else:
        print("Вакансии не найдены по заданным критериям.")


def get_top_n(vacancies: list[Vacancy], n: int) -> list[Vacancy]:
    return sorted(vacancies, key=lambda v: convert_to_rub(v.salary, v.currency), reverse=True)[:n]


def load_currency_rates() -> dict:
    path = "data/currencies.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {c["code"]: 1 / c["rate"] if c["rate"] else 1 for c in raw}


CURRENCY_TO_RUB = load_currency_rates()


def convert_to_rub(salary: int, currency: str) -> int:
    rate = CURRENCY_TO_RUB.get(currency.upper(), 1)
    return int(salary * rate)


def user_delete_vacancy(storage, all_vacancies: list[Vacancy]) -> None:
    indexes_input = input(
        "Введите номера для удаления (например: 1,3,5 или 2-4, или 'all'): "
    ).strip().lower()

    to_delete = set()

    if indexes_input == "all":
        to_delete = set(range(1, len(all_vacancies) + 1))
    else:
        tokens = indexes_input.split(",")
        for token in tokens:
            token = token.strip()
            if "-" in token:
                try:
                    start, end = map(int, token.split("-"))
                    if start > end:
                        start, end = end, start
                    to_delete.update(range(start, end + 1))
                except ValueError:
                    print(f"Неверный диапазон: {token}")
            elif token.isdigit():
                to_delete.add(int(token))
            else:
                print(f"Некорректный ввод: {token}")

    deleted_count = 0
    for idx in sorted(to_delete, reverse=True):
        if 1 <= idx <= len(all_vacancies):
            vacancy = all_vacancies[idx - 1]
            storage.delete_vacancy(vacancy)
            print(f"Удалено: {vacancy.title}")
            deleted_count += 1
        else:
            print(f"Неверный номер: {idx}")

    if deleted_count == 0:
        print("️Ни одна вакансия не была удалена.")
