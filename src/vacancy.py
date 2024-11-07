class Validator:
    """
    Класс валидации параметров для передачи в атрибуты экземпляров класса вакансий.
    В задачу класса входит выбрать из всего набора ключей, полученных от API, те ключи, которые в дальнейшем будут
    использоваться в работе данного приложения.
    -------------------------------------------------------------------------------------------------------------------
    * Каждая вакансия представляет собой словарь с указанными ключами:
    * 'id', 'premium', 'name', 'department', 'has_test', 'response_letter_required', 'area', 'salary', 'type',
    * 'address', 'response_url', 'sort_point_distance', 'published_at', 'created_at', 'archived',
    * 'apply_alternate_url', 'insider_interview', 'url', 'alternate_url', 'relations', 'employer', 'snippet',
    * 'contacts', 'schedule', 'working_days', 'working_time_intervals', 'working_time_modes', 'accept_temporary',
    * 'professional_roles', 'accept_incomplete_resumes', 'experience', 'employment', 'adv_response_url',
    * 'is_adv_vacancy', 'adv_context', 'show_logo_in_search', 'branding'.
    * Выбираются ключи:
    * 'id', 'name', 'salary' (Внутри содержит вложенный словарь {'from' и 'to'}, разделяется на ключи 'salary_from' и
    * 'salary_to'), 'published_at', 'archived', 'apply_alternate_url', 'snippet' (Внутри содержит вложенный словарь
    * {'requirement' и 'responsibility'}, разделяется на ключи 'requirement' и 'responsibility'.
    -------------------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def validate(vacancy_params: dict) -> dict:
        """
        Производит выборку по ключам словаря вакансии и создаёт новых словарь с выбранными ключами и их значениями.
        @param vacancy_params: Содержит параметры одной вакансии.
        @return: Отобранные и валидные параметры одной вакансии.
        """
        # __required_keys = ("id", "name", "salary", "published_at", "archived", "apply_alternate_url", "snippet")
        __slots__ = (
            "id",
            "name",
            "salary_from",
            "salary",
            "published_at",
            "archived",
            "apply_alternate_url",
            "snippet",
        )

        new_vacancy_params = {}
        for key, value in vacancy_params.items():
            if key in __slots__:

                if key == "salary":
                    if vacancy_params[key] is None:
                        new_vacancy_params["salary_from"] = 0
                        new_vacancy_params["salary_to"] = 0
                        new_vacancy_params["currency"] = 0
                    else:
                        new_vacancy_params["salary_from"] = vacancy_params[key]["from"]
                        new_vacancy_params["salary_to"] = vacancy_params[key]["to"]
                        new_vacancy_params["currency"] = vacancy_params[key]["currency"]

                        if vacancy_params[key]["from"] is None:
                            new_vacancy_params["salary_from"] = 0

                        if vacancy_params[key]["to"] is None:
                            new_vacancy_params["salary_to"] = 0

                elif key == "snippet":
                    if vacancy_params[key] is None:
                        new_vacancy_params["requirement"] = 0
                        new_vacancy_params["responsibility"] = 0
                    else:
                        new_vacancy_params["requirement"] = vacancy_params[key]["requirement"]
                        new_vacancy_params["responsibility"] = vacancy_params[key]["responsibility"]

                elif key == "apply_alternate_url":
                    new_vacancy_params["url"] = value

                else:
                    new_vacancy_params[key] = value

        return new_vacancy_params


# ---------------------------------------------------------------------------------------------------------------------
class Vacancy:
    """Класс вакансий. Экземпляр класса представляет собой объект, созданный из элементов JSON-файла, полученного
    в результате запроса на сайт вакансий."""

    obj_vacancies_list: list = []  # Список экземпляров класса Vacancy (объектов вакансий)

    def __init__(self, params: dict) -> None:
        """
        Инициализация экземпляра класса.
        @param params: Параметры вакансии.
        """
        self.id = params["id"]
        self.name = params["name"]
        self.salary_from = params["salary_from"]
        self.salary_to = params["salary_to"]
        self.currency = params["currency"]
        self.published_at = params["published_at"]
        self.archived = params["archived"]
        self.url = params["url"]
        self.requirement = params["requirement"]
        self.responsibility = params["responsibility"]
        # Добавляем вакансию в общий список вакансий
        Vacancy.obj_vacancies_list.append(self)

    def __str__(self) -> str:
        """
        Выводит строковое представление экземпляра класса.
        @return: Строковое представление экземпляра класса.
        """
        return (
            f"ID {self.id}, НАЗВАНИЕ: {self.name}, ЗАРПЛАТА: {self.salary_from} - {self.salary_to} руб, "
            f"URL: {self.url}, ОПУБЛИКОВАН: {self.published_at}, ТРЕБОВАНИЯ: {self.requirement}, "
            f"КОМПЕТЕНЦИИ: {self.responsibility}"
        )

    def __repr__(self):
        """
        Выводит альтернативное строковое представление экземпляра класса.
        @return: Альтернативное строковое представление (develop) экземпляра класса.
        """
        return f"{self.__dict__}"

    def __eq__(self, other) -> bool:
        """
        Осуществляет сравнение экземпляров класса по трём параметрам: начальной зарплате, конечной зарплате и \
        валюте: они равны?
        @param other: Указатель на второй экземпляр класса, с которым происходит сравнение.
        @return: Булево значение результата сравнения двух вакансий по ключам salary_from и salary_to при условии\
        равенства ключей currency.
        """
        return (
            self.currency == other.currency
            and self.salary_from == other.salary_from
            and self.salary_to == other.salary_to
        )

    def __lt__(self, other) -> bool:
        """
        Осуществляет сравнение экземпляров класса по трём параметрам: начальной зарплате, конечной зарплате и \
        валюте: первый меньше, чем второй?
        @param other: Указатель на второй экземпляр класса, с которым происходит сравнение.
        @return: Булево значение результата сравнения двух вакансий по ключам salary_from и salary_to при условии\
        равенства ключей currency.
        """
        return (
            self.currency == other.currency
            and self.salary_from < other.salary_from
            and self.salary_to < other.salary_to
        )

    def __gt__(self, other) -> bool:
        """
        Осуществляет сравнение экземпляров класса по трём параметрам: начальной зарплате, конечной зарплате и \
        валюте: первый больше, чем второй?
        @param other: Указатель на второй экземпляр класса, с которым происходит сравнение.
        @return: Булево значение результата сравнения двух вакансий по ключам salary_from и salary_to при условии\
        равенства ключей currency.
        """
        return (
            self.currency == other.currency
            and self.salary_from > other.salary_from
            and self.salary_to > other.salary_to
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list[dict]) -> None:
        """
        Осуществляет списковое создание экземпляров класса.
        @param vacancies_data: Список вакансий в виде списка словарей для инициализации экземпляров класса.
        @return: None
        """
        for data_item in vacancies_data:
            cls(data_item)

    @classmethod
    def print_obj_vacancies_list(cls) -> None:
        """
        Выводит на экран список строковых представлений экземпляров вакансий.
        @return: None
        """
        for vacancy in cls.obj_vacancies_list:
            print(vacancy)

    @staticmethod
    def print_vacancies_list(data: list[dict], rows_to_print: int | None = None) -> None:
        """
        Выводит на экран список вакансий (список словарей).
        @param data: Список вакансий (список словарей).
        @param rows_to_print: Определяет сколько элементов от начала списка вывести на экран.
        @return: None
        """
        if not data:
            print("Список пуст!")
        else:
            counter = 0
            for data_row in data:
                print(data_row)
                counter += 1
                if counter == rows_to_print:
                    break

    @classmethod
    def __obj_vacancies_list_to_list_dicts(cls) -> list[dict]:
        """
        Приводит список экземпляров вакансий к списку словарей.
        @return: Список вакансий в виде списка словарей.
        """
        result = [current_obj.__dict__ for current_obj in cls.obj_vacancies_list]

        return result

    @classmethod
    def __list_dicts_to_obj_vacancies_list(cls, dicts_list: list[dict]) -> None:
        """
        Приводит список словарей к списку экземпляров класса Vacancy.
        @param dicts_list: Список словарей.
        @return: Список экземпляров класса Vacancy.
        """
        cls.obj_vacancies_list = []
        for current_dict in dicts_list:
            cls(current_dict)

    @classmethod
    def sort_vacancies_by_keyword(cls, key_word: str, top_n: int = 1, save_result: bool = False) -> None:
        """
        Сортирует список вакансий по заданному ключевому слову.
        @param key_word: Определяет ключ, по которому будет производиться сортировка.
        @param top_n: Определяет количество вакансий для вывода на экран.
        @param save_result: Определяет нужно ли сохранить отсортированный список в исходный (по умолчанию не нужно).
        @return: None
        """
        # Сохраним список вакансий из списка объектов вакансий
        tmp_vacancies_list = cls.__obj_vacancies_list_to_list_dicts()
        sorted_vacancies_list = []

        # Производим сортировку
        try:
            sorted_vacancies_list = sorted(tmp_vacancies_list, key=lambda x: x[key_word], reverse=True)
        except KeyError:
            print(f"Ключевое слово '{key_word}' не найдено в списке вакансий!")
        else:
            # Выведем отсортированный список на экран. Если задан параметр top_n, то выведем первые top_n элементов.
            cls.print_vacancies_list(sorted_vacancies_list, top_n)

        # Сохраним отсортированный список вакансий в список объектов вакансий, если установлен флаг must_save и
        # отсортированный список не пустой.
        if save_result and sorted_vacancies_list:
            cls.__list_dicts_to_obj_vacancies_list(sorted_vacancies_list)

    @classmethod
    def filter_vacancies_by_keyword(cls, words: list[str], save_result: bool = False) -> None:
        """
        Фильтрует список вакансий по заданному ключевому слову.
        @param words: Ключевые слова, по которым будет производиться фильтрование.
        @param save_result: Определяет нужно ли сохранять результат фильтрации в исходном списке.
        @return: None
        """
        # Сохраним список вакансий из списка объектов вакансий
        tmp_vacancies_list = cls.__obj_vacancies_list_to_list_dicts()
        filtered_vacancies_list = []

        # Производим фильтрацию
        try:
            for vacancy in tmp_vacancies_list:
                for word in words:
                    if word.lower() in vacancy["name"].lower():
                        filtered_vacancies_list.append(vacancy)
        except KeyError:
            print(f"Список слов для фильтрации '{words}' пуст!")
        else:
            # Выведем отфильтрованный список на экран
            cls.print_vacancies_list(filtered_vacancies_list)

        # Сохраним отфильтрованный список вакансий в список объектов вакансий, если установлен флаг must_save и
        # отсортированный список не пустой.
        if save_result and filtered_vacancies_list:
            cls.__list_dicts_to_obj_vacancies_list(filtered_vacancies_list)

    @classmethod
    def filter_vacancies_by_salary_diapason(cls, srange: str, save_result: bool = False) -> None:
        """
        Фильтрует список вакансий по диапазону зарплат.
        @param srange: Определяет диапазон зарплат.
        @param save_result: Определяет нужно ли сохранять результат фильтрации в исходном списке.
        @return: None
        """
        # Сохраним список вакансий из списка объектов вакансий
        tmp_vacancies_list = cls.__obj_vacancies_list_to_list_dicts()
        filtered_vacancies_list = []

        # Производим фильтрацию
        try:
            left, right = srange.split("-")
            for vacancy in tmp_vacancies_list:
                if vacancy["salary_from"] == int(left.strip()) and vacancy["salary_to"] == int(right.strip()):
                    filtered_vacancies_list.append(vacancy)
        except KeyError:
            print(f"Диапазон {srange} не найден в списке вакансий!")
        else:
            # Выведем отфильтрованный список на экран
            cls.print_vacancies_list(filtered_vacancies_list)

        # Сохраним отфильтрованный список вакансий в список объектов вакансий, если установлен флаг must_save и
        # отсортированный список не пустой.
        if save_result and filtered_vacancies_list:
            cls.__list_dicts_to_obj_vacancies_list(filtered_vacancies_list)


if __name__ == "__main__":
    validator = Validator()

    print("Создадим первую вакансию")
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
            "requirement": "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать \
            навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением...",
            "responsibility": "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. \
            Оценивать инфраструктуру района: ежедневно ходить на...",
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
    print(vacancy1)
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
            "requirement": "Способен работать в команде. Способен принимать решения самостоятельно. Готов учиться и \
            узнавать новое. Опыт работы в колл-центре или службе...",
            "responsibility": "Работать с клиентами или партнерами для решения разнообразных ситуаций. Совершать \
            звонки по их обращениям и давать письменные ответы. ",
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
    print(vacancy2)
    print(repr(vacancy2))
    print()

    print("Сравним две вакансии по зарплате")
    print(vacancy1 == vacancy2)
    print()

    print("Список вакансий формируется внутри класса")
    print("Выведем его на экран")
    Vacancy.print_obj_vacancies_list()
    print()

    print("Внутри класса Vacancy из json-объекта создадим список объектов вакансий и выведем его на экран")
    print("Есть список сырых вакансий, полученных из API")
    hh_vacancies = [
        {
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
                "requirement": "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. \
                Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным \
                мышлением...",
                "responsibility": "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в \
                спальне. Оценивать инфраструктуру района: ежедневно ходить на...",
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
        },
        {
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
                "requirement": "Способен работать в команде. Способен принимать решения самостоятельно. Готов \
                учиться и узнавать новое. Опыт работы в колл-центре или службе...",
                "responsibility": "Работать с клиентами или партнерами для решения разнообразных ситуаций. Совершать \
                звонки по их обращениям и давать письменные ответы. ",
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
        },
        {
            "id": "92223870",
            "premium": False,
            "name": "Удаленный специалист службы поддержки (в Яндекс)",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "113", "name": "Россия", "url": "https://api.hh.ru/areas/113"},
            "salary": {"from": 30000, "to": 44000, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-25T17:39:01+0300",
            "created_at": "2024-01-25T17:39:01+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92223870",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92223870?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92223870",
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
                "requirement": "Способен работать в команде. Способен принимать решения самостоятельно. Готов \
                учиться и узнавать новое. Опыт работы в колл-центре или службе...",
                "responsibility": "Работать с клиентами или партнерами для решения разнообразных ситуаций. Совершать \
                звонки по их обращениям и давать письменные ответы. ",
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
        },
        {
            "id": "92752367",
            "premium": False,
            "name": "Менеджер по продажам недвижимости",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "159", "name": "Астана", "url": "https://api.hh.ru/areas/159"},
            "salary": {"from": 500000, "to": 1000000, "currency": "KZT", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-06T11:30:02+0300",
            "created_at": "2024-02-06T11:30:02+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92752367",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92752367?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92752367",
            "relations": [],
            "employer": {
                "id": "1418491",
                "name": "Витрина Недвижимости",
                "url": "https://api.hh.ru/employers/1418491",
                "alternate_url": "https://hh.ru/employer/1418491",
                "logo_urls": {
                    "240": "https://hhcdn.ru/employer-logo/2935217.jpeg",
                    "90": "https://hhcdn.ru/employer-logo/2935216.jpeg",
                    "original": "https://hhcdn.ru/employer-logo-original/623516.jpg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=1418491",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Отличные коммуникативные навыки, способность найти подход к каждому клиенту. Навыки \
                проведения деловых переговоров. Наличие амбициозных целей и успешный опыт их...",
                "responsibility": "Анализ рынка и объектов недвижимости. Предварительная оценка недвижимости. Подбор \
                объектов недвижимости в интересах клиентов. Консультирование клиентов по купле-продаже объектов...",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "6", "name": "Агент по недвижимости"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "92223673",
            "premium": False,
            "name": "Менеджер чатов, удалённо (в Яндекс)",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "113", "name": "Россия", "url": "https://api.hh.ru/areas/113"},
            "salary": {"from": 30000, "to": 44000, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-25T17:34:32+0300",
            "created_at": "2024-01-25T17:34:32+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92223673",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92223673?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92223673",
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
                "requirement": "Способен работать в команде. Способен принимать решения самостоятельно. Готов \
                учиться и узнавать новое. Опыт работы в колл-центре или службе...",
                "responsibility": "Работать с клиентами или партнерами для решения разнообразных ситуаций. Совершать \
                звонки по их обращениям и давать письменные ответы. ",
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
        },
        {
            "id": "93209001",
            "premium": False,
            "name": "Бортпроводник",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "2759", "name": "Ташкент", "url": "https://api.hh.ru/areas/2759"},
            "salary": None,
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-14T12:32:06+0300",
            "created_at": "2024-02-14T12:32:06+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93209001",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93209001?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93209001",
            "relations": [],
            "employer": {
                "id": "4621904",
                "name": "«MY FREIGHTER» LLC",
                "url": "https://api.hh.ru/employers/4621904",
                "alternate_url": "https://hh.ru/employer/4621904",
                "logo_urls": {
                    "90": "https://hhcdn.ru/employer-logo/3387665.png",
                    "240": "https://hhcdn.ru/employer-logo/3387666.png",
                    "original": "https://hhcdn.ru/employer-logo-original/736672.png",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=4621904",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Образование: среднее полное (11 классов), среднее специальное, высшее. Обязательное \
                владение узбекским, русским и английским языками. Готовность работать согласно графику полетов. ",
                "responsibility": "Обеспечение безопасности на борту. Встреча и размещение пассажиров на борту. \
                Инструктаж перед взлетом. Организация питания пассажиров во время полета. ",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "159", "name": "Бортпроводник"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "92195003",
            "premium": False,
            "name": "Наборщик текста/верстальщик",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "1002", "name": "Минск", "url": "https://api.hh.ru/areas/1002"},
            "salary": {"from": 800, "to": None, "currency": "BYR", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-25T11:58:58+0300",
            "created_at": "2024-01-25T11:58:58+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92195003",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92195003?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92195003",
            "relations": [],
            "employer": {
                "id": "3814315",
                "name": "ПроТекст",
                "url": "https://api.hh.ru/employers/3814315",
                "alternate_url": "https://hh.ru/employer/3814315",
                "logo_urls": {
                    "240": "https://hhcdn.ru/employer-logo/3116885.jpeg",
                    "90": "https://hhcdn.ru/employer-logo/3116884.jpeg",
                    "original": "https://hhcdn.ru/employer-logo-original/668938.jpg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=3814315",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "уверенное владение ПЭВМ (программы OCR - FineReader и аналоги, глубокое знание \
                функций MS Word - Вставка, Макет, Конструктор таблиц). - возможность и готовность...",
                "responsibility": "выполнение распознания документов в формате ,pdf, .jpg, .png на русском / \
                английском языке, макетирование и форматирование в MS Word. - ",
            },
            "contacts": None,
            "schedule": {"id": "remote", "name": "Удаленная работа"},
            "working_days": [],
            "working_time_intervals": [
                {
                    "id": "from_four_to_six_hours_in_a_day",
                    "name": "Можно работать сменами по\xa04–6 часов в\xa0день",
                }
            ],
            "working_time_modes": [{"id": "start_after_sixteen", "name": "Можно начинать работать после 16:00"}],
            "accept_temporary": False,
            "professional_roles": [{"id": "84", "name": "Оператор ПК, оператор базы данных"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "part", "name": "Частичная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93166058",
            "premium": False,
            "name": "Менеджер по продажам (МЕРКАТОР)",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "88", "name": "Казань", "url": "https://api.hh.ru/areas/88"},
            "salary": {"from": 160000, "to": None, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Казань",
                "street": "Приволжский район, жилой массив Отары, Дорожная улица",
                "building": "1к10",
                "lat": 55.724135,
                "lng": 49.098078,
                "description": None,
                "raw": "Казань, Приволжский район, жилой массив Отары, Дорожная улица, 1к10",
                "metro": None,
                "metro_stations": [],
                "id": "15161689",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-13T19:21:57+0300",
            "created_at": "2024-02-13T19:21:57+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93166058",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93166058?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93166058",
            "relations": [],
            "employer": {
                "id": "1060821",
                "name": "Рост Развитие Решение",
                "url": "https://api.hh.ru/employers/1060821",
                "alternate_url": "https://hh.ru/employer/1060821",
                "logo_urls": {
                    "90": "https://hhcdn.ru/employer-logo/874868.jpeg",
                    "240": "https://hhcdn.ru/employer-logo/874869.jpeg",
                    "original": "https://hhcdn.ru/employer-logo-original/85446.jpg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=1060821",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Опыт в продажах. Опыт работы с клиентами. Умение проводить переговоры. Мобильность.",
                "responsibility": "Расширение клиентской базы. Проведение презентаций и переговоров. Заключение \
                договоров. Отчетность в установленной форме.",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "70", "name": "Менеджер по продажам, менеджер по работе с клиентами"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "91178034",
            "premium": False,
            "name": "Оператор call-центра",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "2759", "name": "Ташкент", "url": "https://api.hh.ru/areas/2759"},
            "salary": {"from": 3500000, "to": 20000000, "currency": "UZS", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-25T10:10:00+0300",
            "created_at": "2024-01-25T10:10:00+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=91178034",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/91178034?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/91178034",
            "relations": [],
            "employer": {
                "id": "9522635",
                "name": "IN-FIN-STROY INVEST",
                "url": "https://api.hh.ru/employers/9522635",
                "alternate_url": "https://hh.ru/employer/9522635",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=9522635",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Пожалуйста ознакомьтесь внимательно. Грамотная речь. Знание узбекского и русского \
                языков. Отличное знание ПК. Коммуникабельность. Эмоциональная устойчивость. Вежливость, грамотность, \
                любознательность, ответственность...",
                "responsibility": "Прием и обработка входящих звонков и исходящих звонков. Консультирование \
                клиентов по телефону. Предоставление клиентам информации о компании. Осуществление исходящих \
                информационных...",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "83", "name": "Оператор call-центра, специалист контактного центра"}],
            "accept_incomplete_resumes": True,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "92818620",
            "premium": False,
            "name": "Менеджер по работе с клиентами",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "159", "name": "Астана", "url": "https://api.hh.ru/areas/159"},
            "salary": {"from": 418500, "to": 1000000, "currency": "KZT", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Астана",
                "street": "улица Анет баба",
                "building": "5",
                "lat": 51.133893,
                "lng": 71.382854,
                "description": None,
                "raw": "Астана, улица Анет баба, 5",
                "metro": None,
                "metro_stations": [],
                "id": "14393855",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-07T11:34:26+0300",
            "created_at": "2024-02-07T11:34:26+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92818620",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92818620?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92818620",
            "relations": [],
            "employer": {
                "id": "10013830",
                "name": "Агентство Недвижимости Абажур",
                "url": "https://api.hh.ru/employers/10013830",
                "alternate_url": "https://hh.ru/employer/10013830",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=10013830",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Не важно есть опыт у тебя или нет, я могу точно сказать, что ты сможешь зарабатывать \
                в этой сфере!!! ",
                "responsibility": None,
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "70", "name": "Менеджер по продажам, менеджер по работе с клиентами"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93119114",
            "premium": False,
            "name": "Стажер",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "2759", "name": "Ташкент", "url": "https://api.hh.ru/areas/2759"},
            "salary": {"from": 2000000, "to": 2000000, "currency": "UZS", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Ташкент",
                "street": "улица Мукими",
                "building": "166",
                "lat": 41.295692,
                "lng": 69.218247,
                "description": None,
                "raw": "Ташкент, улица Мукими, 166",
                "metro": None,
                "metro_stations": [],
                "id": "5906580",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-13T08:39:43+0300",
            "created_at": "2024-02-13T08:39:43+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93119114",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93119114?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93119114",
            "relations": [],
            "employer": {
                "id": "3927191",
                "name": "Научно информационный центр новых технологий при ГНК РУз",
                "url": "https://api.hh.ru/employers/3927191",
                "alternate_url": "https://hh.ru/employer/3927191",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=3927191",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Если вы , в том числе, студент по направлению IT или начинающий специалист, \
                окончивший вуз, Вы можете принять участие в отборе...",
                "responsibility": "Комплексная оценка будет проводиться в форме собеседования. Стажировка по \
                направлениям Java-backend и Mobile разработчик (flutter). Участие в непосредственной работе...",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "96", "name": "Программист, разработчик"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "probation", "name": "Стажировка"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "92405436",
            "premium": False,
            "name": "Хозработник",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "2", "name": "Санкт-Петербург", "url": "https://api.hh.ru/areas/2"},
            "salary": {"from": 65000, "to": 70000, "currency": "RUR", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Санкт-Петербург",
                "street": "Бармалеева улица",
                "building": "11",
                "lat": 59.964485,
                "lng": 30.306571,
                "description": None,
                "raw": "Санкт-Петербург, Бармалеева улица, 11",
                "metro": None,
                "metro_stations": [],
                "id": "11151437",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-30T12:59:55+0300",
            "created_at": "2024-01-30T12:59:55+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92405436",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92405436?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92405436",
            "relations": [],
            "employer": {
                "id": "3474160",
                "name": "Нордстрой",
                "url": "https://api.hh.ru/employers/3474160",
                "alternate_url": "https://hh.ru/employer/3474160",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=3474160",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": None,
                "responsibility": "Cезонныe pаботы: убоpкa cнега, лиcтьев, кoшeниe травы, мытьe дoрoжек. Убoрка \
                мусоpа. Прoтиpание пыли, уборка в бapбекю, в бecедке. ",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "32", "name": "Дворник"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "87122346",
            "premium": False,
            "name": "Продавец-консультант",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "1", "name": "Москва", "url": "https://api.hh.ru/areas/1"},
            "salary": {"from": 70000, "to": 110000, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-20T11:00:11+0300",
            "created_at": "2024-02-20T11:00:11+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=87122346",
            "branding": {"type": "MAKEUP", "tariff": None},
            "show_logo_in_search": True,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/87122346?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/87122346",
            "relations": [],
            "employer": {
                "id": "2524051",
                "name": "Магазины Ароматный Мир формата food & wine",
                "url": "https://api.hh.ru/employers/2524051",
                "alternate_url": "https://hh.ru/employer/2524051",
                "logo_urls": {
                    "90": "https://hhcdn.ru/employer-logo/3752459.png",
                    "240": "https://hhcdn.ru/employer-logo/3752460.png",
                    "original": "https://hhcdn.ru/employer-logo-original/827894.png",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=2524051",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Опыт работы не требуется, мы всему научим! Опыт работы в сетевых розничных магазинах \
                приветствуется.",
                "responsibility": "Консультирование покупателей по ассортименту в магазине. Работа на современной и \
                простой кассе. Выкладка продукции, оформление торгового зала рекламными материалами. ",
            },
            "contacts": None,
            "schedule": {"id": "shift", "name": "Сменный график"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "97", "name": "Продавец-консультант, продавец-кассир"}],
            "accept_incomplete_resumes": True,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "77069438",
            "premium": False,
            "name": "Менеджер по туризму",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "160", "name": "Алматы", "url": "https://api.hh.ru/areas/160"},
            "salary": {"from": 180000, "to": 200000, "currency": "KZT", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-02T05:38:18+0300",
            "created_at": "2024-02-02T05:38:18+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=77069438",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/77069438?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/77069438",
            "relations": [],
            "employer": {
                "id": "686727",
                "name": "NurAi & Co",
                "url": "https://api.hh.ru/employers/686727",
                "alternate_url": "https://hh.ru/employer/686727",
                "logo_urls": {
                    "240": "https://hhcdn.ru/employer-logo/1107573.png",
                    "90": "https://hhcdn.ru/employer-logo/1107572.png",
                    "original": "https://hhcdn.ru/employer-logo-original/152128.png",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=686727",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "умение урегулировать форс-мажорные ситуации. - умение работать в системе Битрикс \
                для ведения процесса бронирования. Требования: - опыт работы в туризме обязателен. - ",
                "responsibility": "консультирование клиентов по туристическим продуктам в офисе и по телефону. - \
                обработка входящих заявок и ведение диалога с туристами. - ",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "40", "name": "Другое"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "92210019",
            "premium": False,
            "name": "Junior back-end developer",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "2759", "name": "Ташкент", "url": "https://api.hh.ru/areas/2759"},
            "salary": {"from": 4000000, "to": 8000000, "currency": "UZS", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-01-25T14:24:55+0300",
            "created_at": "2024-01-25T14:24:55+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=92210019",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/92210019?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/92210019",
            "relations": [],
            "employer": {
                "id": "9035038",
                "name": "OOO UZGPS",
                "url": "https://api.hh.ru/employers/9035038",
                "alternate_url": "https://hh.ru/employer/9035038",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=9035038",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Высшее профильное образование. Свободное владение русским и узбекским языками. \
                Java Core. Spring/Spring Boot. Знание ООП и структуры данных. ",
                "responsibility": "Разрабатывать новые и поддерживать существующие продукты компании. Интегрировать \
                сервисы и API. Написание микросервисов. Интеграции с внешними сервисами по REST, WebSocket. ",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "96", "name": "Программист, разработчик"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "noExperience", "name": "Нет опыта"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93523045",
            "premium": False,
            "name": "Менеджер по сопровождению закупок (контрольно-измерительное оборудование)",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "1", "name": "Москва", "url": "https://api.hh.ru/areas/1"},
            "salary": {"from": 90000, "to": None, "currency": "RUR", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": None,
                "street": None,
                "building": None,
                "lat": None,
                "lng": None,
                "description": None,
                "raw": None,
                "metro": {
                    "station_name": "Полежаевская",
                    "line_name": "Таганско-Краснопресненская",
                    "station_id": "7.114",
                    "line_id": "7",
                    "lat": 55.777201,
                    "lng": 37.517895,
                },
                "metro_stations": [
                    {
                        "station_name": "Полежаевская",
                        "line_name": "Таганско-Краснопресненская",
                        "station_id": "7.114",
                        "line_id": "7",
                        "lat": 55.777201,
                        "lng": 37.517895,
                    },
                    {
                        "station_name": "Хорошево",
                        "line_name": "МЦК",
                        "station_id": "95.539",
                        "line_id": "95",
                        "lat": 55.777222,
                        "lng": 37.507222,
                    },
                    {
                        "station_name": "Хорошевская",
                        "line_name": "Большая кольцевая линия",
                        "station_id": "97.601",
                        "line_id": "97",
                        "lat": 55.77643,
                        "lng": 37.51981,
                    },
                ],
                "id": "14977439",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-20T11:07:12+0300",
            "created_at": "2024-02-20T11:07:12+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93523045",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93523045?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93523045",
            "relations": [],
            "employer": {
                "id": "827187",
                "name": "BY business group",
                "url": "https://api.hh.ru/employers/827187",
                "alternate_url": "https://hh.ru/employer/827187",
                "logo_urls": {
                    "original": "https://hhcdn.ru/employer-logo-original/942457.jpg",
                    "240": "https://hhcdn.ru/employer-logo/4210365.jpeg",
                    "90": "https://hhcdn.ru/employer-logo/4210364.jpeg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=827187",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Высшее или средне-специальное образование. Опыт работы на позиции менеджер по \
                закупкам от 3 лет. Знание программы 1С (Управление...",
                "responsibility": "Получать и обрабатывать заявки. Обеспечивать своевременные поставки ТМЦ \
                Заказчикам (закупка оборудования КИПиА и комплектующих). Контролировать поставки и своевременное \
                выполнение обязанностей...",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "66", "name": "Менеджер по закупкам"}],
            "accept_incomplete_resumes": True,
            "experience": {"id": "between3And6", "name": "От 3 до 6 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93514566",
            "premium": False,
            "name": "Водитель-помощник",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "159", "name": "Астана", "url": "https://api.hh.ru/areas/159"},
            "salary": {"from": 300000, "to": None, "currency": "KZT", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Астана",
                "street": "улица Сауран",
                "building": "3",
                "lat": 51.125657,
                "lng": 71.421976,
                "description": None,
                "raw": "Астана, улица Сауран, 3",
                "metro": None,
                "metro_stations": [],
                "id": "816768",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-20T09:52:02+0300",
            "created_at": "2024-02-20T09:52:02+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93514566",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93514566?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93514566",
            "relations": [],
            "employer": {
                "id": "2842834",
                "name": "SNK CONSULT GROUP",
                "url": "https://api.hh.ru/employers/2842834",
                "alternate_url": "https://hh.ru/employer/2842834",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=2842834",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Знание английского языка (B2). Хорошие знание города ПДД. Готовность к \
                командировкам, в том числе за границу. Пунктуальность. ",
                "responsibility": "Мелкосрочный ремонт авто.",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "21", "name": "Водитель"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93254580",
            "premium": False,
            "name": "Машинист буровой установки RU-75",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "102", "name": "Хабаровск", "url": "https://api.hh.ru/areas/102"},
            "salary": {"from": 228000, "to": 228000, "currency": "RUR", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Хабаровск",
                "street": "улица Истомина",
                "building": "51А",
                "lat": 48.474997,
                "lng": 135.058846,
                "description": None,
                "raw": "Хабаровск, улица Истомина, 51А",
                "metro": None,
                "metro_stations": [],
                "id": "4898993",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-15T08:00:54+0300",
            "created_at": "2024-02-15T08:00:54+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93254580",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93254580?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93254580",
            "relations": [],
            "employer": {
                "id": "4987434",
                "name": "Охотская Горно-Геологическая Компания",
                "url": "https://api.hh.ru/employers/4987434",
                "alternate_url": "https://hh.ru/employer/4987434",
                "logo_urls": {
                    "original": "https://hhcdn.ru/employer-logo-original/944456.jpg",
                    "240": "https://hhcdn.ru/employer-logo/4218361.jpeg",
                    "90": "https://hhcdn.ru/employer-logo/4218360.jpeg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=4987434",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Квалификационное удостоверение машиниста буровой установки 5 разряда. Опыт работы \
                на буровой установки RU-75., LM-75. Проведение текущих аварийных и...",
                "responsibility": "Бурение из буровых камер. Бурение согласно ГТН, умение подобрать \
                породоразрушающий инструмент, монтаж на устье скважины.",
            },
            "contacts": None,
            "schedule": {"id": "flyInFlyOut", "name": "Вахтовый метод"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "63", "name": "Машинист"}],
            "accept_incomplete_resumes": True,
            "experience": {"id": "between3And6", "name": "От 3 до 6 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93545071",
            "premium": False,
            "name": "Семейный водитель",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "1", "name": "Москва", "url": "https://api.hh.ru/areas/1"},
            "salary": {"from": 120000, "to": 120000, "currency": "RUR", "gross": False},
            "type": {"id": "open", "name": "Открытая"},
            "address": None,
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-20T14:19:36+0300",
            "created_at": "2024-02-20T14:19:36+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93545071",
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93545071?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93545071",
            "relations": [],
            "employer": {
                "id": "2021156",
                "name": "ТТО АМИК",
                "url": "https://api.hh.ru/employers/2021156",
                "alternate_url": "https://hh.ru/employer/2021156",
                "logo_urls": None,
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=2021156",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "опыт работы профессиональным водителем от 10 лет, семейным водителем - от 5 лет. \
                - наличие рекомендательных писем (обязательно). - спокойное,комфортное и безопасное...",
                "responsibility": "работа в качестве семейного водителя. - подача автомобиля по указанному месту в \
                обозначенное время. - планирование оптимального маршрута движения. - выполнение поручений \
                профессионального...",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "21", "name": "Водитель"}],
            "accept_incomplete_resumes": True,
            "experience": {"id": "moreThan6", "name": "Более 6 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
        {
            "id": "93161709",
            "premium": False,
            "name": "Менеджер по работе с клиентами (МЕРКАТОР)",
            "department": None,
            "has_test": False,
            "response_letter_required": False,
            "area": {"id": "88", "name": "Казань", "url": "https://api.hh.ru/areas/88"},
            "salary": {"from": 100000, "to": None, "currency": "RUR", "gross": True},
            "type": {"id": "open", "name": "Открытая"},
            "address": {
                "city": "Казань",
                "street": "Приволжский район, жилой массив Отары, Дорожная улица",
                "building": "1к10",
                "lat": 55.724135,
                "lng": 49.098078,
                "description": None,
                "raw": "Казань, Приволжский район, жилой массив Отары, Дорожная улица, 1к10",
                "metro": None,
                "metro_stations": [],
                "id": "15161689",
            },
            "response_url": None,
            "sort_point_distance": None,
            "published_at": "2024-02-13T17:06:04+0300",
            "created_at": "2024-02-13T17:06:04+0300",
            "archived": False,
            "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93161709",
            "show_logo_in_search": None,
            "insider_interview": None,
            "url": "https://api.hh.ru/vacancies/93161709?host=hh.ru",
            "alternate_url": "https://hh.ru/vacancy/93161709",
            "relations": [],
            "employer": {
                "id": "1060821",
                "name": "Рост Развитие Решение",
                "url": "https://api.hh.ru/employers/1060821",
                "alternate_url": "https://hh.ru/employer/1060821",
                "logo_urls": {
                    "90": "https://hhcdn.ru/employer-logo/874868.jpeg",
                    "240": "https://hhcdn.ru/employer-logo/874869.jpeg",
                    "original": "https://hhcdn.ru/employer-logo-original/85446.jpg",
                },
                "vacancies_url": "https://api.hh.ru/vacancies?employer_id=1060821",
                "accredited_it_employer": False,
                "trusted": True,
            },
            "snippet": {
                "requirement": "Опыт в продажах или с клиентами. Грамотная речь. Активность. Коммуникабельность.",
                "responsibility": "Работа с клиентами. Контроль остатков инструмента на складе. Работа с дебиторской \
                задолженностью. Отчетность в установленной форме (1С, Битрикс 24).",
            },
            "contacts": None,
            "schedule": {"id": "fullDay", "name": "Полный день"},
            "working_days": [],
            "working_time_intervals": [],
            "working_time_modes": [],
            "accept_temporary": False,
            "professional_roles": [{"id": "70", "name": "Менеджер по продажам, менеджер по работе с клиентами"}],
            "accept_incomplete_resumes": False,
            "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
            "employment": {"id": "full", "name": "Полная занятость"},
            "adv_response_url": None,
            "is_adv_vacancy": False,
            "adv_context": None,
        },
    ]

    print("Проведём валидацию этого списка и внутри класса Vacancy создадим экземпляры класса")
    validated_vacancies = [validator.validate(item) for item in hh_vacancies]
    Vacancy.cast_to_object_list(validated_vacancies)

    print("Выведем на экран в виде списка созданные вакансии")
    print(Vacancy.print_obj_vacancies_list())
    print()

    n = 5
    print(f"Выведем на экран список из ТОП-{n} вакансий")
    Vacancy.sort_vacancies_by_keyword("salary_from", n)
    print("Выведем на экран строковые представления вакансий")
    Vacancy.print_obj_vacancies_list()
    print()

    filter_words = ["стажер", "developer"]
    print(f"Выведем на экран список вакансий отфильтрованных по словам {filter_words}")
    Vacancy.filter_vacancies_by_keyword(filter_words)
    print()

    salary_range = "500000 - 1000000"
    print(f"Выведем на экран список вакансий отфильтрованных по диапазону зарплат {salary_range}")
    Vacancy.filter_vacancies_by_salary_diapason(salary_range)
    print()
