from src.file_worker import JsonWorker, CsvWorker, ExcelWorker
from src.headhunter_api import HeadHunterAPI
from src.json_saver import JsonSaver
from src.vacancy import Validator, Vacancy

from tqdm import tqdm

import time

BASE_URL = "https://api.hh.ru/vacancies"

# Пример работы конструктора класса с одной вакансией
print("#" + "*" * 100)
print("Пример работы классов Validator и Vacancy с одной вакансией")
print("Полученные из API в виде json-объекта вакансии нуждаются в валидации (удаление ненужных ключей и реформат)")
print("Для решения этой задачи создан класс Validator")
print("Описание класса Validator:")
print(Validator.__doc__)
validator = Validator()
print()

print("Проверим работу классов Validator и Vacancy")
print("Создадим одну вакансию")
pd1 = {
    "id": "93353083",
    "premium": False,
    "name": "Тестировщик комфорта квартир",
    "department": None,
    "has_test": False,
    "response_letter_required": False,
    "area": {"id": "26", "name": "Воронеж", "url": "https://api.hh.ru/areas/26"},
    "salary": {"from": 350000, "to": 450000, "currency": "RUR", "gross": False},
    "type": {"id": "open", "name": "Открытая"},
    "address": None,
    "response_url": None,
    "sort_point_distance": None,
    "published_at": "2024-02-16T14:58:28+0300",
    "created_at": "2024-02-16T14:58:28+0300",
    "archived": False,
    "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93353083",
    "branding": {"type": "CONSTRUCTOR", "tariff": "BASIC"},
    "show_logo_in_search": True,
    "insider_interview": None,
    "url": "https://api.hh.ru/vacancies/93353083?host=hh.ru",
    "alternate_url": "https://hh.ru/vacancy/93353083",
    "relations": [],
    "employer": {
        "id": "3499705",
        "name": "Специализированный застройщик BM GROUP",
        "url": "https://api.hh.ru/employers/3499705",
        "alternate_url": "https://hh.ru/employer/3499705",
        "logo_urls": {
            "original": "https://hhcdn.ru/employer-logo-original/1214854.png",
            "240": "https://hhcdn.ru/employer-logo/6479866.png",
            "90": "https://hhcdn.ru/employer-logo/6479865.png",
        },
        "vacancies_url": "https://api.hh.ru/vacancies?employer_id=3499705",
        "accredited_it_employer": False,
        "trusted": True,
    },
    "snippet": {
        "requirement": "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением...",
        "responsibility": "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на...",
    },
    "contacts": None,
    "schedule": {"id": "flexible", "name": "Гибкий график"},
    "working_days": [],
    "working_time_intervals": [],
    "working_time_modes": [],
    "accept_temporary": False,
    "professional_roles": [{"id": "107", "name": "Руководитель проектов"}],
    "accept_incomplete_resumes": False,
    "experience": {"id": "noExperience", "name": "Нет опыта"},
    "employment": {"id": "full", "name": "Полная занятость"},
    "adv_response_url": None,
    "is_adv_vacancy": False,
    "adv_context": None,
}
validated_pd1 = validator.validate(pd1)
vacancy1 = Vacancy(validated_pd1)
print("Проверим работу __str__")
print(vacancy1)
print("Проверим работу repr")
print(repr(vacancy1))
print()

print("Создадим вторую вакансию")
pd2 = {
    "id": "92223756",
    "premium": False,
    "name": "Удаленный диспетчер чатов (в Яндекс)",
    "department": None,
    "has_test": False,
    "response_letter_required": False,
    "area": {"id": "113", "name": "Россия", "url": "https://api.hh.ru/areas/113"},
    "salary": {"from": 30000, "to": 44000, "currency": "RUR", "gross": True},
    "type": {"id": "open", "name": "Открытая"},
    "address": None,
    "response_url": None,
    "sort_point_distance": None,
    "published_at": "2024-01-25T17:37:04+0300",
    "created_at": "2024-01-25T17:37:04+0300",
    "archived": False,
    "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92223756",
    "show_logo_in_search": None,
    "insider_interview": None,
    "url": "https://api.hh.ru/vacancies/92223756?host=hh.ru",
    "alternate_url": "https://hh.ru/vacancy/92223756",
    "relations": [],
    "employer": {
        "id": "9498120",
        "name": "Яндекс Команда для бизнеса",
        "url": "https://api.hh.ru/employers/9498120",
        "alternate_url": "https://hh.ru/employer/9498120",
        "logo_urls": {
            "original": "https://hhcdn.ru/employer-logo-original/1121425.jpg",
            "90": "https://hhcdn.ru/employer-logo/6106293.jpeg",
            "240": "https://hhcdn.ru/employer-logo/6106294.jpeg",
        },
        "vacancies_url": "https://api.hh.ru/vacancies?employer_id=9498120",
        "accredited_it_employer": False,
        "trusted": True,
    },
    "snippet": {
        "requirement": "Способен работать в команде. Способен принимать решения самостоятельно. Готов учиться и узнавать новое. Опыт работы в колл-центре или службе...",
        "responsibility": "Работать с клиентами или партнерами для решения разнообразных ситуаций. Совершать звонки по их обращениям и давать письменные ответы. ",
    },
    "contacts": None,
    "schedule": {"id": "remote", "name": "Удаленная работа"},
    "working_days": [],
    "working_time_intervals": [],
    "working_time_modes": [{"id": "start_after_sixteen", "name": "Можно начинать работать после 16:00"}],
    "accept_temporary": False,
    "professional_roles": [{"id": "40", "name": "Другое"}],
    "accept_incomplete_resumes": True,
    "experience": {"id": "noExperience", "name": "Нет опыта"},
    "employment": {"id": "full", "name": "Полная занятость"},
    "adv_response_url": None,
    "is_adv_vacancy": False,
    "adv_context": None,
}
validated_pd2 = validator.validate(pd2)
vacancy2 = Vacancy(validated_pd2)
print("Проверим работу __str__")
print(vacancy2)
print("Проверим работу repr")
print(repr(vacancy2))
print()

print("Сравним две вакансии по зарплате")
print("Платят одинаково?")
# Работает метод __eq__
print(["Нет!", "Да!"][vacancy1 == vacancy2])
print("За первую ваканcию платят меньше?")
# Работает метод __lt__
print(["Нет!", "Да!"][vacancy1 < vacancy2])
print("Выходит, за первую платят больше?")
# Работает метод __gt__
print(["Нет!", "Да!"][vacancy1 > vacancy2])
print()

# Сохранение информации о вакансиях в файл
print("Сохранение информации о вакансиях в файл")
print("Алгоритм записи в файл: из экземпляра класса Vacancy создаём json-объект и затем записываем его в файл")
print("Создадим конструктор класса JsonSaver")
json_saver = JsonSaver()
print("Запишем первый экземпляр класса Vacancy в json-объект")
json_saver.add_vacancy(vacancy1)
print("Добавим второй экземпляр класса Vacancy в json-объект")
json_saver.add_vacancy(vacancy2)

print("Запишем полученный json-объект в json-файл")
json_worker = JsonWorker("data/data.json")
try:
    json_worker.write_file(json_saver.json_list)
except Exception as e:
    print(e)
else:
    print(f"Файл {"data/data.json"} успешно записан")

print("Запишем полученный json-объект в csv-файл")
csv_worker = CsvWorker("data/data.csv")
try:
    csv_worker.write_file(json_saver.json_list)
except Exception as e:
    print(e)
else:
    print(f"Файл {"data/data.csv"} успешно записан")

print("Запишем полученный json-объект в excel-файл")
excel_worker = ExcelWorker("data/data.xlsx")
try:
    excel_worker.write_file(json_saver.json_list)
except Exception as e:
    print(e)
else:
    print(f"Файл {"data/data.xlsx"} успешно записан")
finally:
    print("Работа file_worker завершена")
print()

# Функция для взаимодействия с пользователем
print("#" + "*" * 100)
print("Теперь осуществим реальный запрос к API и проверим работу классов")
print("Готовность...")
time.sleep(2)
print("#" + "*" * 100)
print()


def user_interaction() -> None:
    """
    Функция взаимодействует с пользователем.
    @return: None
    """
    # Блок получения от пользователя входных данных
    # -----------------------------------------------------------------------------------------------------------------
    print("Сначала запросим у пользователя входные данные для запроса")
    time.sleep(2)
    user_input = input("Введите поисковый запрос (default 'Python') >>: ")  # Пример: "Python"
    keyword = "Python" if not user_input else user_input

    user_input = input("Ведите количество желаемых страниц (default 100) >>: ")
    vacancies_number = 100 if not user_input else int(user_input)

    user_input = input("Введите количество вакансий для вывода в топ N по зарплате (default 5) >>: ")
    top_n = 5 if not user_input else user_input

    user_input = input(
        "Введите ключевые слова для фильтрации вакансий (Пример: back-end стажер) >>: "
    ).split()  # Пример: back-end стажер
    filter_words = ["back-end", "стажер"] if not user_input else user_input

    user_input = input("Введите диапазон зарплат (Пример: 100000 - 150000) >>: ")  # Пример: 100000 - 150000
    salary_range = "100000 - 150000" if not user_input else user_input
    print()
    # -----------------------------------------------------------------------------------------------------------------

    print("Задача 1 - Подключимся к API и получим вакансии")
    print("Создадим экземпляр класса для работы с API сайтов с вакансиями")
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    # url = "https://api.hh.ru/vacancies" определяет, что поиск вакансий будет производиться на всех сайтах группы
    # компаний HeadHunter. Если необходимо локализовать поиск, то можно использовать варианты:
    # "https://api.hh.kz/vacancies"
    # "https://api.headhunter.kg/vacancies" т.д. Подробнее в документации на сайте компании.
    print("Получим сырые данные из API")
    try:
        hh_api = HeadHunterAPI(url=BASE_URL, per_page=vacancies_number)
    except ConnectionError:
        print("Дальше нет смысла... Выходим")
        exit(1)

    # Получение вакансий с hh.ru в формате JSON
    # Аргумент query, полученный от пользователя, определяет слово, по которому будет осуществлён поиск.
    # Аргумент pages определяет количество страниц, в которых будет осуществлён поиск.
    print("Загрузим вакансии из API в json-объект")
    hh_vacancies = hh_api.load_vacancies(keyword=keyword)

    print("Выведем элементы полученного json-объекта по одному для демонстрации")
    for vacancy in hh_vacancies:
        print(vacancy, end="\n")

    # Пример работы конструктора класса со списком вакансий, полученных из API
    print("#" + "*" * 100)
    print("Задача 2 - из полученных из API данных создадим экземпляры класса Vacancy")
    print("Создадим список объектов", end=" ")
    validated_vacancies = [validator.validate(item) for item in hh_vacancies]
    Vacancy.cast_to_object_list(validated_vacancies)
    print("и выведем его на экран")
    print(Vacancy.print_obj_vacancies_list())

    # Запишем экземпляры класса Vacancy в json-объект
    print("Запишем экземпляры класса Vacancy в json-объект")
    for vacancy in Vacancy.obj_vacancies_list:
        json_saver.add_vacancy(vacancy)

    # Запишем в json-файл
    print("Запишем полученный json-объект в json-файл", end="\n")
    try:
        json_worker.write_file(json_saver.json_list)
        for _ in tqdm(range(100)):
            time.sleep(0.02)
    except Exception as ex:
        print(ex)
    else:
        print(f"Файл {"data/data.json"} успешно записан")

    # Запишем в csv-файл
    print("Запишем в csv-файл", end="\n")
    try:
        csv_worker.write_file(json_saver.json_list)
        for _ in tqdm(range(100)):
            time.sleep(0.02)
    except Exception as ex:
        print(ex)
    else:
        print(f"Файл {"data/data.csv"} успешно записан")

    # Запишем в Excel-файл
    print("Запишем в Excel-файл", end="\n")
    try:
        excel_worker.write_file(json_saver.json_list)
        for _ in tqdm(range(100)):
            time.sleep(0.02)
    except Exception as ex:
        print(ex)
    else:
        print(f"Файл {"data/data.xlsx"} успешно записан")
    finally:
        print("Работа file_worker завершена")
    print()

    # Выведем на экран список ТОП вакансий отсортированных по заработной плате
    print(f"Отсортируем вакансии по заработной плате и выведем на экран ТОП-{top_n} вакансий")
    Vacancy.sort_vacancies_by_keyword("salary_from", top_n)
    print()

    # Выведем на экран список вакансий отфильтрованных по ключевым словам
    print(f"Выведем на экран список вакансий отфильтрованных по словам {filter_words}")
    Vacancy.filter_vacancies_by_keyword(filter_words)
    print()

    # Выведем на экран список вакансий отфильтрованный по диапазону зарплат
    print(f"Выведем на экран список вакансий отфильтрованных по диапазону зарплат {salary_range}")
    Vacancy.filter_vacancies_by_salary_diapason(salary_range)
    print()


if __name__ == "__main__":
    user_interaction()
