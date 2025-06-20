import pytest
from src.models.vacancy import Vacancy


@pytest.mark.parametrize("salary_data, expected", [
    (100_000, (100_000, 0, "RUR")),
    ({"from": 120_000, "to": 150_000, "currency": "USD"}, (120_000, 150_000, "USD")),
    ({"from": None, "to": None, "currency": None}, (0, 0, "RUR")),
    ("invalid", (0, 0, "RUR")),
])
def test_parse_salary_variants(salary_data, expected):
    assert Vacancy._parse_salary(salary_data) == expected


@pytest.mark.parametrize("salary_data, expected_string", [
    ({"from": 100_000}, "от 100000 RUB"),
    ({"to": 80_000}, "до 80000 RUB"),
    ({"from": 50_000, "to": 70_000}, "50000 – 70000 RUB"),
    ({}, "зарплата не указана"),
])
def test_str_salary_display(salary_data, expected_string):
    v = Vacancy("Dev", "url", salary_data, "1 год", "Москва", "Полная")
    assert expected_string in str(v)


def test_str_foreign_currency(monkeypatch):
    monkeypatch.setattr("src.utils.helpers.convert_to_rub", lambda a, c: a * 90)

    v = Vacancy("Dev", "url", {"from": 100, "to": 200, "currency": "USD"}, "3+", "СПб", "Стажировка")
    text = str(v)
    assert "~9000" in text and "18000" in text


def test_to_dict_and_from_dict_roundtrip():
    v = Vacancy("Dev", "url", {"from": 100_000, "to": 120_000}, "1+", "Москва", "Удалённо")
    d = v.to_dict()
    restored = Vacancy.from_dict(d)
    assert restored.title == v.title
    assert restored.salary_from == v.salary_from
    assert restored.salary_to == v.salary_to
    assert restored.currency == v.currency
    assert restored.area == v.area


def test_str_only_rub_from(monkeypatch):
    monkeypatch.setattr("src.utils.helpers.convert_to_rub", lambda a, c: 10000 if a else None)
    v = Vacancy("Test", "url", {"from": 100, "currency": "USD"}, "1+", "Москва", "Полная")
    result = str(v)
    assert "(~10000 руб.)" in result


def test_str_only_rub_to(monkeypatch):
    monkeypatch.setattr("src.utils.helpers.convert_to_rub", lambda a, c: 20000 if a else None)
    v = Vacancy("Test", "url", {"to": 200, "currency": "USD"}, "1+", "Москва", "Полная")
    result = str(v)
    assert "(~20000 руб.)" in result
