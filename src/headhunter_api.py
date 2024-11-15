import requests

from abc import ABC, abstractmethod

BASE_URL = "https://api.hh.ru/vacancies"


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list:
        """Обязательный метод для получения списка вакансий.
        @param keyword: Строковая переменная, содержащая ключевое слово, по которому осуществляется первичный отбор
        вакансий.
        @return: Список вакансий.
        """
        ...


# ---------------------------------------------------------------------------------------------------------------------
class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self, url: str = BASE_URL, per_page: int = 1) -> None:
        """
        Инициализатор экземпляра класса.
        @param url: URL-адрес для GET-запроса. По умолчанию "https://api.hh.ru/vacancies" - все сайты группы компаний.
        HeadHunter. Возможны варианты выбора ...api.hh.kz/... или ...api.headhunter.kg/... (Подробнее в документации
        на сайте компании).
        @param per_page: Количество вакансий на странице. По умолчанию - 1 (Подробнее в документации на сайте
        компании).
        """
        self.__url = url
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": per_page, "only_with_salary": True}
        self.__vacancies: list = []

    def __connect_to_api(self) -> requests.models.Response | None:
        """
        Метод для подключения к API и проверки статус-кода.
        @return:
        """
        try:
            response = requests.get(self.__url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def load_vacancies(self, keyword: str = "Python") -> list[dict]:
        """
        Метод для получения списка вакансий.
        @param keyword: Строковая переменная, содержащая ключевое слово, по которому осуществляется первичный отбор
        вакансий.
        @return: Список вакансий.
        """
        response = self.__connect_to_api()
        if response is None:
            return []

        self.__params["text"] = keyword
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        vacancies = response.json()
        self.__vacancies = vacancies.get("items", [])

        return self.__vacancies


if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    print("Получим сырые данные из API")
    hh_api = HeadHunterAPI(url=BASE_URL, per_page=100)

    # Получение вакансий с hh.ru в формате JSON
    # -----------------------------------------------------------------------------------------------------------------
    # Аргумент keyword определяет слово, по которому будет осуществлён поиск.
    # Аргумент pages определяет количество страниц, в которых будет осуществлён поиск.
    # -----------------------------------------------------------------------------------------------------------------
    hh_vacancies = hh_api.load_vacancies(keyword="Python")
    for vacancy in hh_vacancies:
        print(vacancy, end="\n")
