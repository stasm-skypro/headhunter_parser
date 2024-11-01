from abc import ABC


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    def load_vacancies(self, keyword: str) -> list:
        """Обязательный метод для получения списка вакансий"""
        ...
