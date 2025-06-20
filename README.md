# 🧠 Проект: Поиск вакансий с hh.ru

![Тесты](https://github.com/serge23023/Project_2_vacancy-search/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/serge23023/Project_2_vacancy-search/branch/main/graph/badge.svg)](https://codecov.io/gh/serge23023/Project_2_vacancy-search)

Интеграция с HeadHunter API: поиск, фильтрация, сохранение и удаление вакансий.  
Консольное приложение, реализованное с применением ООП, SOLID и покрытое тестами.

---

## 📦 Poetry и зависимости

Зависимости проекта управляются через `pyproject.toml`.

```bash
poetry install
```

---

## ▶️ Запуск

```bash
poetry run python main.py
```

---

## 📁 Структура проекта

```
.
├── main.py                          # Точка входа
├── pyproject.toml                   # Зависимости и метаданные проекта
│
├── src/
│   ├── api/
│   │   ├── base_api.py             # Абстрактный API-класс
│   │   ├── hh_api.py               # Класс для работы с hh.ru
│   │   └── area_lookup.py          # Работа с регионами
│   ├── interface/
│   │   └── user_interface.py       # Меню пользователя
│   ├── models/
│   │   └── vacancy.py              # Модель вакансии
│   ├── storage/
│   │   ├── base_storage.py         # Абстрактное хранилище
│   │   └── json_storage.py         # Работа с JSON-файлом
│   └── utils/
│       ├── helpers.py              # Фильтрация, сортировка, удаление
│       └── currency_loader.py      # Загрузка валют с API
│
├── data/
│   ├── areas.json                  # Справочник регионов (автоматически)
│   ├── currencies.json             # Курсы валют (автоматически)
│   └── vacancies.json              # Сохранённые вакансии
│
└── tests/
    ├── test_area_lookup.py
    ├── test_currency_loader.py
    ├── test_helpers.py
    ├── test_json_storage.py
    ├── test_user_interface.py
    ├── test_vacancy.py
    ├── test_base_api.py
    ├── test_base_storage.py
```

---

## 🧪 Тестирование

```bash
poetry run pytest --cov=src
```

- Покрытие кода: **>95%**
- Используются `pytest`, `pytest-cov`, `monkeypatch`, `capsys`, `tmp_path`

---

## 🧾 Особенности

- Полностью реализовано через ООП
- Использован `__slots__`, `@property`, `@classmethod`
- Чтение и сохранение вакансий в JSON
- Автоматическая конвертация валют
- Фильтрация по ключевым словам, региону, опыту, занятости
- Подключён CI и покрытие

---

## 📄 Лицензия

MIT — свободно для использования в учебных целях