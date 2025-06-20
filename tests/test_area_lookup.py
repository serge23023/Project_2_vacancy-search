import json
import os
import tempfile
import pytest
import requests

from src.api.area_lookup import (
    flatten_areas, suggest_areas_by_input,
    get_area_id_from_user_input, load_areas
)

AREAS = [
    {
        "id": "1", "name": "Россия",
        "areas": [
            {"id": "2", "name": "Москва", "areas": []},
            {"id": "3", "name": "Санкт-Петербург", "areas": []}
        ]
    }
]


@pytest.fixture(autouse=True)
def mock_areas(monkeypatch):
    monkeypatch.setattr("src.api.area_lookup.load_areas", lambda: AREAS)


def test_flatten_areas():
    flat = flatten_areas(AREAS)
    assert len(flat) == 3
    assert any(a["name"] == "Москва" for a in flat)


def test_suggest_area_found():
    assert suggest_areas_by_input("моск")[0]["name"] == "Москва"


def test_suggest_area_not_found():
    assert suggest_areas_by_input("Томск") == []


@pytest.mark.parametrize("user_input, expected", [
    ("Санкт", "3"),                # одна запись
    ("Неизвестный", None),        # ничего не найдено
])
def test_get_area_id_single_cases(user_input, expected):
    assert get_area_id_from_user_input(user_input) == expected


def test_get_area_id_multiple_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")  # выбираем СПб
    assert get_area_id_from_user_input("с") == "3"


@pytest.mark.parametrize("fake_input", ["abc", "999"])
def test_get_area_id_multiple_invalid(monkeypatch, fake_input):
    monkeypatch.setattr("builtins.input", lambda _: fake_input)
    assert get_area_id_from_user_input("с") is None


def test_load_areas_from_file(monkeypatch):
    data = [{"id": "123", "name": "Тест"}]
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name

    monkeypatch.setattr("src.api.area_lookup.AREA_FILE", path)
    assert load_areas() == data
    os.remove(path)


def test_load_areas_from_api(monkeypatch):
    dummy = [{"id": "999", "name": "Москва"}]

    class MockResponse:
        def raise_for_status(self): pass
        @staticmethod
        def json(): return dummy

    monkeypatch.setattr("src.api.area_lookup.os.path.exists", lambda _: False)
    monkeypatch.setattr("src.api.area_lookup.requests.get", lambda _: MockResponse())
    monkeypatch.setattr("src.api.area_lookup.AREA_FILE", tempfile.mktemp())

    assert load_areas() == dummy


def test_load_areas_api_failure(monkeypatch, capsys):
    def fail_get(url):
        raise requests.RequestException(url)

    monkeypatch.setattr("src.api.area_lookup.os.path.exists", lambda _: False)
    monkeypatch.setattr("src.api.area_lookup.requests.get", fail_get)
    monkeypatch.setattr("src.api.area_lookup.AREA_FILE", tempfile.mktemp())

    result = load_areas()
    captured = capsys.readouterr()

    assert result == []
    assert "Ошибка загрузки" in captured.out
