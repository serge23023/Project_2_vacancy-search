from src.interface.user_interface import run
from src.models.vacancy import Vacancy


# Dummy API, Storage и Patch Map
class DummyAPI:
    @staticmethod
    def get_vacancies(*args, **kwargs):
        return [
            {"name": "Python Dev", "alternate_url": "url", "salary": {"from": 100000},
             "experience": {"name": "1"}, "area": {"name": "Москва"}, "employment": {"name": "Полная"}}
        ]


class DummyStorage:
    def __init__(self):
        self.saved = []
        self.deleted = []

    def add_vacancy(self, v): self.saved.append(v)

    def get_vacancies(self): return self.saved

    def delete_vacancy(self, v): self.deleted.append(v)


# -------------------------------
# SCENARIO: Найти и сохранить вакансии
# -------------------------------

def test_run_find_and_save(monkeypatch, capsys):
    inputs = iter([
        "1",  # Меню: Найти
        "2",  # Опыт: 1-3 года
        "90000",  # Зарплата
        "y",  # Только с зп
        "Москва",  # Регион
        "Python",  # Запрос
        "0"  # Выход
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.interface.user_interface.HeadHunterAPI", lambda: DummyAPI())
    monkeypatch.setattr("src.interface.user_interface.JSONStorage", lambda: DummyStorage())
    monkeypatch.setattr("src.interface.user_interface.get_area_id_from_user_input", lambda x: "1")

    run()
    out = capsys.readouterr().out
    assert "Сохранено 1 вакансий" in out


# -------------------------------
# SCENARIO: Показать топ N (пусто)
# -------------------------------

def test_run_show_empty(monkeypatch, capsys):
    inputs = iter(["2", "", "", "", "", "", "3", "0"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.interface.user_interface.JSONStorage", lambda: DummyStorage())

    run()
    out = capsys.readouterr().out
    assert "вакансии не найдены" in out.lower()


# -------------------------------
# SCENARIO: Удалить без вакансий
# -------------------------------

def test_run_delete_empty(monkeypatch, capsys):
    inputs = iter(["3", "0"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.interface.user_interface.JSONStorage", lambda: DummyStorage())

    run()
    out = capsys.readouterr().out
    assert "нет сохранённых вакансий" in out.lower()


# -------------------------------
# SCENARIO: Удаление из списка
# -------------------------------

def test_run_delete_existing(monkeypatch, capsys):
    storage = DummyStorage()
    storage.saved.append(Vacancy("Python", "url", {"from": 100000}, "1", "Москва", "Полная"))

    inputs = iter(["3", "1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.interface.user_interface.JSONStorage", lambda: storage)

    run()
    assert len(storage.deleted) == 1


# -------------------------------
# SCENARIO: Неверный ввод меню
# -------------------------------

def test_run_invalid_choice(monkeypatch, capsys):
    inputs = iter(["99", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.interface.user_interface.JSONStorage", lambda: DummyStorage())

    run()
    out = capsys.readouterr().out
    assert "неверный ввод" in out.lower()
