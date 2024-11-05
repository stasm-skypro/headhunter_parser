import csv
import json
import os
from abc import ABC, abstractmethod

import pandas as pd


class FileWorker(ABC):
    """Класс для работы с файлами: записи в файл данных и чтения данных из файла."""

    @abstractmethod
    def write_file(self, data: list):
        """Абстрактный метод для записи списка словарей в файл. Подлежит переопределению в классе-наследнике."""
        ...

    # @abstractmethod
    # def get_data_from_file(self, filter_words: list[str]) -> list:
    #     """Абстрактный метод для получения данных из файла по критериям"""
    #
    # @abstractmethod
    # def delete_data_from_file(self,  id: str) -> None:
    #     """Абстрактный метод для удаления данных из файла"""


class JsonWriter(FileWorker):
    """Класс для записи списка словарей в json-файл."""

    def __init__(self, file_name: str) -> None:
        """Инициализатор экземпляра класса."""
        self.file_name = file_name

    def write_file(self, data: list) -> None:
        """Записывает список словарей в json-файл."""
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)


class CsvWriter(FileWorker):
    """Класс для записи списка словарей в csv-файл."""

    def __init__(self, file_name: str) -> None:
        """Инициализатор экземпляра класса."""
        self.file_name = file_name

    @staticmethod
    def get_field_names(data: list) -> list:
        """Создаёт список заголовков csv-файла."""
        result = [key for key in data[0].keys()]

        return result

    def write_file(self, data: list) -> None:
        """Записывает список словарей в csv-файл."""
        field_names = self.get_field_names(data)
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", newline="", encoding="UTF-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for row_dict in data:
                writer.writerow(row_dict)


class ExcelWriter(FileWorker):
    """Класс для записи списка словарей в xlsx-файл."""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def write_file(self, data: list) -> None:
        """Записывает список словарей в xlsx-файл."""
        df = pd.DataFrame(data)
        full_path = os.path.abspath(self.file_name)
        df.to_excel(full_path, index=False)


if __name__ == "__main__":
    from src.headhunter_api import HeadHunterAPI
    from src.validator import Validator

    print("Получим сырые данные из API")
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)

    validator = Validator()
    # Из исходного списка словарей, полученных из API, соберём новый список словарей с выбранными ключами.
    validated_vacancies = [validator.validate(item) for item in hh_vacancies]

    # Запишем в json-файл
    print("Запишем в json-файл", end="\n")
    json_worker = JsonWriter("../data/data.json")
    json_worker.write_file(validated_vacancies)

    # Запишем в csv-файл
    print("Запишем в csv-файл", end="\n")
    csv_worker = CsvWriter("../data/data.csv")
    csv_worker.write_file(validated_vacancies)

    # Запишем в Excel-файл
    print("Запишем в Excel-файл", end="\n")
    excel_worker = ExcelWriter("../data/data.xlsx")
    excel_worker.write_file(validated_vacancies)
