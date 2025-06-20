import requests
from src.api.hh_api import HeadHunterAPI


def test_get_vacancies_success(monkeypatch):
    def mock_get(url, params):
        assert url == HeadHunterAPI.BASE_URL
        assert params["text"] == "Python"
        assert params["per_page"] == 20
        assert params["experience"] == "between1And3"
        assert params["salary"] == 150000
        assert params["only_with_salary"] == "True"
        assert params["area"] == "1"

        class MockResponse:
            def raise_for_status(self): pass
            def json(self): return {"items": [{"name": "Dev"}]}
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    api = HeadHunterAPI()
    result = api.get_vacancies(
        keyword="Python",
        experience="between1And3",
        salary=150000,
        only_with_salary=True,
        area="1"
    )

    assert isinstance(result, list)
    assert result[0]["name"] == "Dev"


def test_get_vacancies_failure(monkeypatch, capsys):
    def fail_get(url, params=None):
        raise requests.RequestException("boom")

    monkeypatch.setattr("requests.get", fail_get)

    api = HeadHunterAPI()
    result = api.get_vacancies("Python")

    captured = capsys.readouterr()
    assert "Ошибка при подключении" in captured.out
    assert result == []
