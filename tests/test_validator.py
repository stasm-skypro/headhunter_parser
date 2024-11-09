import pytest
from src.vacancy import Validator


@pytest.fixture
def sample_vacancy() -> dict:
    """
    Фикстура параметров сырой вакансии.
    @return: None
    """
    return {
        "id": "123",
        "name": "Python Developer",
        "salary": {"from": 100000, "to": 200000, "currency": "RUR"},
        "published_at": "2023-01-01",
        "archived": False,
        "apply_alternate_url": "http://example.com/apply",
        "snippet": {
            "requirement": "3+ years of experience",
            "responsibility": "Develop software",
        },
        "premium": True,
        "department": None,
        # остальные ключи не имеют значения для теста
    }


def test_validate(sample_vacancy: dict) -> None:
    """
    Проверяет работу метода 'validate' (из сырых параметров вакансии должен получится набор нужных ключей).
    @param sample_vacancy:  Фикстура параметров сырой вакансии.
    @return:
    """
    validated = Validator.validate(sample_vacancy)

    expected = {
        "id": "123",
        "name": "Python Developer",
        "salary_from": 100000,
        "salary_to": 200000,
        "currency": "RUR",
        "published_at": "2023-01-01",
        "archived": False,
        "url": "http://example.com/apply",
        "requirement": "3+ years of experience",
        "responsibility": "Develop software",
    }

    assert validated == expected


def test_validate_with_missing_keys(sample_vacancy: dict) -> None:
    """
    Проверяет работу метода 'validate' (из сырых параметров вакансии должен получится набор нужных ключей),
    при условии отсутствия некоторых ключей.
    @param sample_vacancy:  Фикстура параметров сырой вакансии.
    @return: None
    """
    del sample_vacancy["salary"]
    del sample_vacancy["snippet"]

    validated = Validator.validate(sample_vacancy)

    expected = {
        "id": "123",
        "name": "Python Developer",
        "published_at": "2023-01-01",
        "archived": False,
        "url": "http://example.com/apply",
    }

    assert validated == expected
