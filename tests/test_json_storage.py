import os
import tempfile
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


def test_add_and_delete_vacancy():
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    storage = JSONStorage(filename=tmp_file.name)

    v = Vacancy("Test", "link", {"from": 100}, "1", "Москва", "Полная")
    storage.add_vacancy(v)

    all_v = storage.get_vacancies()
    assert len(all_v) == 1

    storage.delete_vacancy(v)
    all_v = storage.get_vacancies()
    assert len(all_v) == 0

    tmp_file.close()
    os.remove(tmp_file.name)


def test_json_storage_creates_file(tmp_path):
    path = tmp_path / "new.json"
    assert not path.exists()

    from src.storage.json_storage import JSONStorage
    store = JSONStorage(str(path))

    assert path.exists()
    assert path.read_text(encoding="utf-8") == "[]"


def test_json_storage_invalid_json(tmp_path, capsys):
    path = tmp_path / "bad.json"
    path.write_text("INVALID_JSON", encoding="utf-8")

    from src.storage.json_storage import JSONStorage
    store = JSONStorage(str(path))
    result = store.get_vacancies()

    assert result == []
    assert "Ошибка чтения JSON" in capsys.readouterr().out
