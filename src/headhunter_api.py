import requests

from src.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self, url="https://api.hh.ru/vacancies", per_page=1):
        """
        Инициализатор экземпляра класса.
        :param url: URL-адрес для GET-запроса. По умолчанию "https://api.hh.ru/vacancies" - все сайты группы компаний.
        HeadHunter. Возможны варианты выбора ...api.hh.kz/... или ...api.headhunter.kg/... (Подробнее в документации
        на сайте компании).
        :param per_page: Количество вакансий на странице. По умолчанию - 1 (Подробнее в документации на сайте
        компании).
        """
        self.url = url
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": per_page, "items": [{}]}
        self.vacancies = []

    def load_vacancies(self, keyword: str, pages: int = 1) -> list[dict]:
        """
        Метод для получения списка вакансий.
        :param keyword: Строковая переменная, содержащая ключевое слово, по которому осуществляется первичный отбор
        вакансий.
        :param pages: целочисленный аргумент, определяющий число страниц, на которых будет осуществлён поиск.
        :return: Список вакансий
        """
        self.params["text"] = keyword
        while self.params.get("page") != pages:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.params["page"] += 1

        return self.vacancies


if __name__ == "__main__":

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    # -----------------------------------------------------------------------------------------------------------------
    # url = "https://api.hh.ru/vacancies" определяет, что поиск вакансий будет производиться на всех сайтах группы
    # компаний HeadHunter. Если необходимо локализовать поиск, то можно использовать варианты:
    # "https://api.hh.kz/vacancies"
    # "https://api.headhunter.kg/vacancies" т.д. Подробнее в документации на сайте компании.
    # -----------------------------------------------------------------------------------------------------------------
    print("Получим сырые данные из API")
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)

    # Получение вакансий с hh.ru в формате JSON
    # -----------------------------------------------------------------------------------------------------------------
    # Аргумент keyword определяет слово, по которому будет осуществлён поиск.
    # Аргумент pages определяет количество страниц, в которых будет осуществлён поиск.
    # -----------------------------------------------------------------------------------------------------------------
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)
    for vacancy in hh_vacancies:
        print(vacancy, end="\n")
