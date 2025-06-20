import pytest
import builtins
from src.utils.helpers import *
from src.models.vacancy import Vacancy


def make(title="Dev", sal=100000, cur="RUR", exp="1", area="Москва", emp="Полная"):
    return Vacancy(title, "url", {"from": sal, "currency": cur}, exp, area, emp)


# --------------------
# BASIC FILTER TESTS
# --------------------

def test_convert_to_rub(monkeypatch):
    monkeypatch.setattr("src.utils.helpers.CURRENCY_TO_RUB", {"USD": 90})
    assert convert_to_rub(100, "USD") == 9000
    assert convert_to_rub(100, "XXX") == 100


@pytest.mark.parametrize("query,count", [
    (["Python"], 1), (["Dev"], 3), (["Scala"], 0)
])
def test_filter_by_keywords(query, count):
    data = [make("Python Dev"), make("Java Dev"), make("JS Dev")]
    assert len(filter_by_keywords(data, query)) == count


@pytest.mark.parametrize("input_str,expected", [
    ("70000-150000", 2),
    ("abc-def", 3),
    ("100000", 3)
])
def test_filter_by_salary(input_str, expected, capsys):
    data = [make(sal=100000), make(sal=80000), make(sal=200000, cur="USD")]
    assert len(filter_by_salary(data, input_str)) == expected


def test_filter_by_experience():
    data = [make(exp="1 год"), make(exp="3 года"), make(exp="Без опыта")]
    assert len(filter_by_experience(data, 2)) == 1


@pytest.mark.parametrize("fn, val, expected", [
    (filter_by_region, "москва", 2),
    (filter_by_employment, "частичная", 1)
])
def test_filter_by_region_and_employment(fn, val, expected):
    data = [make(emp="Полная"), make(emp="Частичная", area="СПб"), make(emp="Стажировка")]
    assert len(fn(data, val)) == expected


def test_get_top_n():
    data = [make(sal=50), make(sal=150), make(sal=100)]
    top = get_top_n(data, 2)
    assert top[0].salary_from == 150


def test_to_vacancy_objects():
    valid = [{
        "name": "Python",
        "alternate_url": "url",
        "salary": {"from": 100000},
        "experience": {"name": "1"},
        "area": {"name": "Москва"},
        "employment": {"name": "Полная"}
    }]
    zero = [{**valid[0], "salary": {}}]
    assert len(to_vacancy_objects(valid)) == 1
    assert to_vacancy_objects(zero) == []


def test_load_currency_rates(monkeypatch, tmp_path):
    path = tmp_path / "currencies.json"
    path.write_text(json.dumps([{"code": "USD", "rate": 0.01}]), encoding="utf-8")
    real_open = builtins.open
    monkeypatch.setattr("src.utils.helpers.os.path.exists", lambda _: True)
    monkeypatch.setattr(builtins, "open", lambda p, *a, **kw: real_open(path, *a, **kw))
    assert load_currency_rates()["USD"] == pytest.approx(100.0)


def test_load_currency_rates_missing(monkeypatch):
    monkeypatch.setattr("src.utils.helpers.os.path.exists", lambda _: False)
    assert load_currency_rates() == {}


# -------------------------
# USER DELETE TESTS
# -------------------------

class Dummy:
    def __init__(self): self.deleted = []
    def delete_vacancy(self, v): self.deleted.append(v)


@pytest.mark.parametrize("user_input,expected", [
    ("all", 3), ("1-2", 2), ("1,3", 2), ("3-1", 3)
])
def test_user_delete_variants(monkeypatch, user_input, expected):
    data = [make("v1"), make("v2"), make("v3")]
    monkeypatch.setattr("builtins.input", lambda _: user_input)
    d = Dummy()
    user_delete_vacancy(d, data)
    assert len(d.deleted) == expected


@pytest.mark.parametrize("text", ["abc", "1-abc", "99"])
def test_user_delete_invalid(monkeypatch, capsys, text):
    monkeypatch.setattr("builtins.input", lambda _: text)
    user_delete_vacancy(Dummy(), [make()])
    out = capsys.readouterr().out.lower()
    assert "некорректный" in out or "неверный" in out


# -------------------------
# APPLY FILTERS FULL FLOW
# -------------------------

@pytest.mark.parametrize("inputs,vacancies,expect", [
    (["Dev", "", "", "", "", "2"],
     [make("Dev"), make("Manager")],
     "топ вакансий"),

    (["", "90000-150000", "", "", "", "2"],
     [make(sal=100000), make(sal=80000)],
     "топ вакансий"),

    (["", "", "3", "", "", "2"],
     [make(exp="1 год"), make(exp="3 года")],
     "топ вакансий"),

    (["", "", "", "Москва", "", "2"],
     [make(area="Москва"), make(area="СПб")],
     "топ вакансий"),

    (["", "", "", "", "Полная", "2"],
     [make(emp="Полная"), make(emp="Частичная")],
     "топ вакансий"),

    (["", "", "", "", "", "abc"],
     [make(), make()],
     "топ вакансий"),

    (["Unicorn", "", "", "", "", "3"],
     [make("Python")],
     "не найдены"),
])
def test_apply_user_filters(monkeypatch, capsys, inputs, vacancies, expect):
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    apply_user_filters(vacancies)
    out = capsys.readouterr().out.lower()
    assert expect.lower() in out
