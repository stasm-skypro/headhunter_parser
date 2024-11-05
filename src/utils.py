def get_top_vacancies(vacancies: list, top: int) -> list:
    """Выводит ТОП вакансий из списка вакансий.
    :vacancies: list[dict] - Список вакансий.
    :top: int - количество вакансий, которое необходимо получить."""
    result = sorted(vacancies, key=lambda x: x["salary_from"])
    return result
