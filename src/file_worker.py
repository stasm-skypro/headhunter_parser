import csv
import json
import os
from abc import ABC, abstractmethod

import pandas as pd


class FileWorker(ABC):
    """Класс для работы с файлами: записи в файл данных и чтения данных из файла."""

    @abstractmethod
    def write_file(self, data: list):
        """Абстрактный метод для json-объекта в файл. Подлежит переопределению в классе-наследнике."""
        ...

    @abstractmethod
    def read_file(self):
        """Абстрактный метод для записи json-объекта в файл. Подлежит переопределению в классе-наследнике."""
        ...


class JsonWorker(FileWorker):
    """Класс для работы json-файлами."""

    def __init__(self, file_name: str) -> None:
        """Инициализатор экземпляра класса."""
        self.file_name = file_name

    def write_file(self, data: list) -> None:
        """Записывает json-объект в json-файл."""
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)

    def read_file(self):
        """Читает содержимое json-файла в json-объект."""
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "r", encoding='utf-8') as file:
            data = json.load(file)

        return data


class CsvWorker(FileWorker):
    """Класс для работы с csv-файлами."""

    def __init__(self, file_name: str) -> None:
        """Инициализатор экземпляра класса."""
        self.file_name = file_name

    @staticmethod
    def get_field_names(data: list) -> list:
        """Создаёт список заголовков csv-файла."""
        return [key for key in data[0].keys()]

    def write_file(self, data: list) -> None:
        """Записывает json-объект в csv-файл."""
        field_names = self.get_field_names(data)
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "w", newline="", encoding="UTF-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for row_dict in data:
                writer.writerow(row_dict)

    def read_file(self):
        """Читает содержимое csv-файла в json-объект."""
        data = []
        full_path = os.path.abspath(self.file_name)
        with open(full_path, "r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(dict(row))

        return data


class ExcelWorker(FileWorker):
    """Класс для работы с xlsx-файлами."""

    def __init__(self, file_name: str) -> None:
        """Инициализатор экземпляра класса."""
        self.file_name = file_name

    def write_file(self, data: list) -> None:
        """Записывает json-объект в xlsx-файл."""
        df = pd.DataFrame(data)
        full_path = os.path.abspath(self.file_name)
        df.to_excel(full_path, index=False)

    def read_file(self):
        """Читает содержимое excel-файла в json-объект."""
        full_path = os.path.abspath(self.file_name)
        df = pd.read_excel(full_path)
        data = df.to_dict(orient='records')

        return data


if __name__ == "__main__":
    from src.headhunter_api import HeadHunterAPI
    from src.validator import Validator

    print("Получим сырые данные из API")
    hh_api = HeadHunterAPI(url="https://api.hh.ru/vacancies", per_page=100)
    hh_vacancies = hh_api.load_vacancies(keyword="Python", pages=1)

    validator = Validator()
    # Из исходного списка словарей, полученных из API, соберём новый список словарей с выбранными ключами.
    validated_vacancies = [validator.validate(item) for item in hh_vacancies]

    # Запишем json-объект в json-файл
    print("Запишем json-объект в json-файл", end="\n")
    json_worker = JsonWorker("../data/data.json")
    json_worker.write_file(validated_vacancies)

    # Прочитаем json-файл в json-объект
    print("Прочитаем json-файл в json-объект и выведем в консоль")
    for item_data in json_worker.read_file():
        print(item_data)

    # Запишем json-объект в csv-файл
    print("Запишем json-объект в csv-файл", end="\n")
    csv_worker = CsvWorker("../data/data.csv")
    csv_worker.write_file(validated_vacancies)

    # Прочитаем csv-файл в json-объект
    print("Прочитаем csv-файл в json-объект и выведем в консоль")
    for item_data in csv_worker.read_file():
        print(item_data)

    # Запишем json-объект в Excel-файл
    print("Запишем json-объект в Excel-файл", end="\n")
    excel_worker = ExcelWorker("../data/data.xlsx")
    excel_worker.write_file(validated_vacancies)

    # Прочитаем Excel-файл в json-объект
    print("Прочитаем Excel-файл в json-объект и выведем в консоль", end="\n")
    for item_data in excel_worker.read_file():
        print(item_data)
