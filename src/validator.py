class Validator:
    """
    Класс валидации параметров для передачи в атрибуты экземпляров класса вакансий.
    В задачу класса входит выбрать из всего набора ключей, полученных от API, те ключи, которые в дальнейшем будут
    использоваться в работе данного приложения.
    *******************************************************************************************************************
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
    *******************************************************************************************************************
    """

    @staticmethod
    def validate(vacancy_params: dict) -> dict:
        """Производит выборку по ключам словаря вакансии и создаёт новых словарь с выбранными ключами и их значениями.
        :vacancy_params: Словарь, содержащий параметры одной вакансии.
        :*required_keys: кортеж, содержащий список ключей, которые необходимо указать в создаваемом словаре с
        параметрами вакансии.
        """
        __required_keys = ("id", "name", "salary", "published_at", "archived", "apply_alternate_url", "snippet")

        new_vacancy_params = {}
        for key, value in vacancy_params.items():
            if key in __required_keys:

                if key == "salary":
                    if vacancy_params[key] is None:
                        new_vacancy_params["salary_from"] = 0
                        new_vacancy_params["salary_to"] = 0
                        new_vacancy_params["currency"] = None
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
                        new_vacancy_params["requirement"] = None
                        new_vacancy_params["responsibility"] = None
                    else:
                        new_vacancy_params["requirement"] = vacancy_params[key]["requirement"]
                        new_vacancy_params["responsibility"] = vacancy_params[key]["responsibility"]

                elif key == "apply_alternate_url":
                    new_vacancy_params["url"] = value

                else:
                    new_vacancy_params[key] = value

        return new_vacancy_params


if __name__ == "__main__":
    # Пример использования
    from src.headhunter_api import HeadHunterAPI

    print("Получим сырые данные из API")
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)

    validator = Validator()
    # Из исходного списка словарей, полученных из API, соберём новый список словарей с выбранными ключами.
    print("Из сырых данных сформируем свой json-объект с нужными данными")
    validated_vacancies = [validator.validate(item) for item in hh_vacancies]
    for item in validated_vacancies:
        print(item)
