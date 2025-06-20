import json
import requests

from src.api.currency_loader import fetch_and_save_currency_rates


def test_fetch_and_save_success(monkeypatch, tmp_path, capsys):
    dummy_currency_data = {
        "currency": [
            {"code": "USD", "rate": 0.012},
            {"code": "RUR", "rate": 1.0},
            {"code": "FAKE", "rate": None}  # должен быть исключён
        ]
    }

    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return dummy_currency_data

    monkeypatch.setattr("src.api.currency_loader.requests.get", lambda _: MockResponse())

    fake_currency_file = tmp_path / "currencies.json"
    monkeypatch.setattr("src.api.currency_loader.CURRENCY_FILE", str(fake_currency_file))
    monkeypatch.setattr("src.api.currency_loader.os.makedirs", lambda *a, **kw: None)

    fetch_and_save_currency_rates()

    # Проверка stdout
    out = capsys.readouterr().out
    assert "успешно обновлены" in out.lower()

    # Проверка содержимого файла
    with open(fake_currency_file, "r", encoding="utf-8") as f:
        saved = json.load(f)
    assert {"code": "USD", "rate": 0.012} in saved
    assert {"code": "RUR", "rate": 1.0} in saved
    assert all("FAKE" not in c["code"] for c in saved)


def test_fetch_and_save_failure(monkeypatch, capsys):
    def fail_get(url):
        raise requests.RequestException("boom")

    monkeypatch.setattr("src.api.currency_loader.requests.get", fail_get)

    fetch_and_save_currency_rates()
    out = capsys.readouterr().out
    assert "ошибка" in out.lower()
    assert "/dictionaries" in out
