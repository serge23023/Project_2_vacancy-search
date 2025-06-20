from src.api.hh_api import HeadHunterAPI
from src.api.area_lookup import get_area_id_from_user_input
from src.utils.helpers import to_vacancy_objects, apply_user_filters, user_delete_vacancy
from src.storage.json_storage import JSONStorage


def run():
    hh = HeadHunterAPI()
    storage = JSONStorage()

    while True:
        print("\n===== Меню =====")
        print("1. Найти и сохранить вакансии")
        print("2. Показать топ N по фильтрам")
        print("3. Удалить вакансию")
        print("0. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            # Фильтр по опыту
            print("Опыт работы:")
            print("1. Нет опыта")
            print("2. 1–3 года")
            print("3. 3–6 лет")
            print("4. Более 6 лет")

            exp_map = {
                "1": "noExperience",
                "2": "between1And3",
                "3": "between3And6",
                "4": "moreThan6"
            }

            exp_choice = input("Выберите уровень опыта (0–4, ENTER чтобы пропустить): ").strip()
            experience_id = exp_map.get(exp_choice)

            salary_input = input("Желаемая зарплата (только число, ENTER чтобы пропустить): ").strip()
            salary = int(salary_input) if salary_input.isdigit() else None

            only_salary = input("Искать только вакансии с зарплатой? (y/n): ").lower().startswith("y")

            area_name = input("Введите регион (например: Москва): ").strip()
            area_id = get_area_id_from_user_input(area_name) if area_name else None

            query = input("Введите поисковый запрос: ")
            results = hh.get_vacancies(
                query,
                experience=experience_id,
                salary=salary,
                only_with_salary=only_salary,
                area=area_id,
            )

            vacancies = to_vacancy_objects(results)
            for v in vacancies:
                storage.add_vacancy(v)

            print(f"Сохранено {len(vacancies)} вакансий.")

        elif choice == "2":
            all_vacancies = storage.get_vacancies()
            apply_user_filters(all_vacancies)

        elif choice == "3":
            all_vacancies = storage.get_vacancies()

            if not all_vacancies:
                print("Нет сохранённых вакансий.")
                continue

            print("\nСписок сохранённых вакансий:")
            for i, v in enumerate(all_vacancies, start=1):
                print(f"{i}. {v}")

            user_delete_vacancy(storage, all_vacancies)

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")
