import csv
import json
import os
from abc import ABC, abstractmethod

import pandas as pd

from src.headhunter_api import HeadHunterAPI


class FileWorker(ABC):
    """Класс для работы с файлами: записи в файл данных и чтения данных из файла."""

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


class CsvWriter(FileWorker):
    def __init__(self, file_name):
        self.file_name = file_name

    @staticmethod
    def get_field_names(data):
        result = []
        for key in data[0].keys():
            result.append(key)
        return result

    def write_file(self, data):
        field_names = self.get_field_names(data)
        field_names.extend(['show_logo_in_search', 'branding'])

        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", newline='', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for row_dict in data:
                writer.writerow(row_dict)


class ExcelWriter(FileWorker):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_file(self, data):
        df = pd.DataFrame(data)
        full_path = os.path.abspath(self.file_name)
        df.to_excel(full_path, index=False)


if __name__ == "__main__":
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)

    # Запишем в json-файл
    print("Запишем в json-файл", end='\n')
    fileworker = JsonWriter("../data/data.json")
    fileworker.write_file(hh_vacancies)

    # Запишем в csv-файл
    print("Запишем в csv-файл", end='\n')
    fileworker = CsvWriter("../data/data.csv")
    fileworker.write_file(hh_vacancies)

    # Запишем в Excel-файл
    print("Запишем в Excel-файл", end='\n')
    fileworker = ExcelWriter("../data/data.xlsx")
    fileworker.write_file(hh_vacancies)
