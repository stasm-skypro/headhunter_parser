import pytest

from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancy_params() -> dict:
    """
    Фикстура для тестирования создания экземпляра класса Vacancy.
    @return: Набор параметров вакансии (обработанных и валидных).
    """
    return {
        "id": "1",
        "name": "Тестировщик комфорта квартир",
        "salary_from": 350000,
        "salary_to": 450000,
        "currency": "RUB",
        "published_at": "2024-02-16T14:58:28+0300",
        "archived": False,
        "url": "https://hh.ru/applicant/vacancy_response?vacancyId=93353083",
        "requirement": "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением...",
        "responsibility": "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на...",
    }


def test_vacancy_initialization(sample_vacancy_params: dict) -> None:
    """
    Проверяем создание экземпляра класса Vacancy из набора параметров (json-объекта).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy = Vacancy(sample_vacancy_params)
    assert vacancy.id == "1"
    assert vacancy.name == "Тестировщик комфорта квартир"
    assert vacancy.salary_from == 350000
    assert vacancy.salary_to == 450000
    assert vacancy.currency == "RUB"
    assert vacancy.published_at == "2024-02-16T14:58:28+0300"
    assert not vacancy.archived
    assert vacancy.url == "https://hh.ru/applicant/vacancy_response?vacancyId=93353083"
    assert (
        vacancy.requirement
        == "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением..."
    )
    assert (
        vacancy.responsibility
        == "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на..."
    )


def test_vacancy_str(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу строковое представление экземпляра вакансии (метод __str__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy = Vacancy(sample_vacancy_params)
    expected_str = (
        "ID 1, НАЗВАНИЕ: Тестировщик комфорта квартир, ЗАРПЛАТА: 350000 - 450000 руб, "
        "URL: https://hh.ru/applicant/vacancy_response?vacancyId=93353083, ОПУБЛИКОВАН: 2024-02-16T14:58:28+0300, "
        "ТРЕБОВАНИЯ: Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением..., "
        "КОМПЕТЕНЦИИ: Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на..."
    )
    assert str(vacancy) == expected_str


def test_vacancy_repr(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу строковое представление экземпляра вакансии (метод __repr__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy = Vacancy(sample_vacancy_params)
    expected_repr = (
        "{'id': '1', 'name': 'Тестировщик комфорта квартир', 'salary_from': 350000, 'salary_to': 450000, "
        "'currency': 'RUB', "
        "'published_at': '2024-02-16T14:58:28+0300', 'archived': False, "
        "'url': 'https://hh.ru/applicant/vacancy_response?vacancyId=93353083', 'requirement': "
        "'Занимать активную жизненную позицию, уметь активно танцевать и громко петь. Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. Обладать системным мышлением...', "
        "'responsibility': 'Оценивать вид из окна: встречать рассветы на кухне, и провожать алые закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на...'}"
    )
    assert repr(vacancy) == expected_repr


def test_vacancy_equality(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу сравнения на эквивалентность экземпляров класса (метод __eq__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy1 = Vacancy(sample_vacancy_params)
    vacancy2 = Vacancy(sample_vacancy_params)
    assert vacancy1 == vacancy2


def test_vacancy_inequality(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу сравнения на эквивалентность экземпляров класса (метод __eq__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy1 = Vacancy(sample_vacancy_params)
    sample_vacancy_params["salary_from"] = 1500
    vacancy2 = Vacancy(sample_vacancy_params)
    assert vacancy1 != vacancy2


def test_vacancy_less_than(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу сравнения на 'меньше' двух экземпляров класса (метод __lt__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy1 = Vacancy(sample_vacancy_params)
    sample_vacancy_params["salary_from"] = 500
    sample_vacancy_params["salary_to"] = 1500
    vacancy2 = Vacancy(sample_vacancy_params)
    assert vacancy2 < vacancy1


def test_vacancy_greater_than(sample_vacancy_params: dict) -> None:
    """
    Проверяет работу сравнения на 'больше' двух экземпляров класса (метод __gt__).
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancy1 = Vacancy(sample_vacancy_params)
    sample_vacancy_params["salary_from"] = 500
    sample_vacancy_params["salary_to"] = 1500
    vacancy2 = Vacancy(sample_vacancy_params)
    assert vacancy1 > vacancy2


def test_cast_to_object_list(sample_vacancy_params: dict) -> None:
    """
    Проверяет создание списка экземпляров вакансий из списка словарей.
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancies_data = [sample_vacancy_params]
    Vacancy.cast_to_object_list(vacancies_data)
    assert len(Vacancy.obj_vacancies_list) == 12
    assert isinstance(Vacancy.obj_vacancies_list[0], Vacancy)


def test_sort_vacancies_by_keyword(sample_vacancy_params: dict) -> None:
    """
    Проверяет сортировку вакансий по критерию 'salary_from'.
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancies_data = [sample_vacancy_params]
    Vacancy.cast_to_object_list(vacancies_data)
    Vacancy.sort_vacancies_by_keyword("salary_from")
    assert Vacancy.obj_vacancies_list[0].salary_from == 350000


def test_filter_vacancies_by_keyword(sample_vacancy_params: dict) -> None:
    """
    Проверяет фильтрацию вакансий по критерию 'name'.
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancies_data = [sample_vacancy_params]
    Vacancy.cast_to_object_list(vacancies_data)
    Vacancy.filter_vacancies_by_keyword(["Python"])
    assert len(Vacancy.obj_vacancies_list) == 14
    assert Vacancy.obj_vacancies_list[0].name == "Тестировщик комфорта квартир"


def test_filter_vacancies_by_salary_diapason(sample_vacancy_params: dict) -> None:
    """
    Проверяет фильтрацию вакансий по критериям 'salary_from' и 'salary_to'.
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @return: None
    """
    vacancies_data = [sample_vacancy_params]
    Vacancy.cast_to_object_list(vacancies_data)
    Vacancy.filter_vacancies_by_salary_diapason("1000-2000")
    assert len(Vacancy.obj_vacancies_list) == 15
    assert Vacancy.obj_vacancies_list[0].salary_from == 350000
    assert Vacancy.obj_vacancies_list[0].salary_to == 450000


def test_delete_vacancy(sample_vacancy_params: dict) -> None:
    """
    Проверяет удаление вакансии.
    @param sample_vacancy_params: Фикстура параметров вакансии.
    @param id: Строковый аргумент - идентификатор вакансии в списке вакансий.
    @return: None
    """
    Vacancy.obj_vacancies_list = []
    vacancies_data = [sample_vacancy_params]
    Vacancy.cast_to_object_list(vacancies_data)
    assert Vacancy.obj_vacancies_list[0].id == "1"
    Vacancy.delete_vacancy("1")
    assert Vacancy.obj_vacancies_list == []
