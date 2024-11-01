
class Validation:
    """Класс """

    def __init__(self) -> None:
        ...

    @staticmethod
    def validate(params: dict):
        for item in params:
            if item == 'apply_alternate_url':
                if params[item] is None:
                    params[item] = "Неизвестный адрес URL"

            if item == 'salary':
                if params[item] is None:
                    params[item] = {"from": 0, "to": 0, "currency": "RUR", "gross": True}

            if item == 'snippet':
                if params[item] is None:
                    params[item] = {
                    "requirement": "Нет требований",
                    "responsibility": "Компетенции не определены",
                }

        return params
