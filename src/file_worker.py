import json
import os
from abc import ABC, abstractmethod

from src.headhunter_api import HeadHunterAPI


class FileWorker(ABC):
    """Класс для работы с файлами: записи в файл данных и чтения даных из файла."""

    @abstractmethod
    def write_file(self, data):
        ...


class JsonWriter(FileWorker):

    def __init__(self, file_name):
        self.file_name = file_name

    def write_file(self, data):
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)




if __name__ == "__main__":
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)

    # Запишем в json-файл
    print("Запишем в json-файл")
    fileworker = JsonWriter("../data/data.json")
    fileworker.write_file(hh_vacancies)
