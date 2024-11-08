from src.json_saver import JsonSaver


# Мок-класс для проверки
class MockVacancy:
    """
    Мок-класс для проверки.
    """

    def __init__(self, name: str, salary: int) -> None:
        """
        Инициализатор экземпляра класса.
        @param title: Название вакансии.
        @param salary: Заработная плата.
        """
        self.title = name
        self.salary = salary


def test_add_vacancy() -> None:
    """
    Проверяем добавление вакансии в экземпляр класса JsonSaver.
    @return: None
    """
    # Создаем экземпляр MockVacancy
    vacancy1 = MockVacancy("Тестировщик комфорта квартир", 450000)

    # Очищаем json_list перед тестом
    JsonSaver.json_list = []

    # Добавляем вакансию
    JsonSaver.add_vacancy(vacancy1)

    # Проверяем, что вакансия была добавлена в json_list
    assert len(JsonSaver.json_list) == 1
    assert JsonSaver.json_list[0]["title"] == "Тестировщик комфорта квартир"
    assert JsonSaver.json_list[0]["salary"] == 450000

    # Добавляем еще одну вакансию
    vacancy2 = MockVacancy("Удаленный диспетчер чатов (в Яндекс)", 120000)
    JsonSaver.add_vacancy(vacancy2)

    # Проверяем, что обе вакансии были добавлены в json_list
    assert len(JsonSaver.json_list) == 2
    assert JsonSaver.json_list[1]["title"] == "Удаленный диспетчер чатов (в Яндекс)"
    assert JsonSaver.json_list[1]["salary"] == 120000
