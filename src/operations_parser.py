import json
from datetime import datetime
from typing import List


def load_operations(file_path: str) -> List:
    """
    Загружает операции из JSON-файла
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def parse_date(date_str: str) -> datetime:
    """
    Парсит строку даты в объект datetime
    """
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))


# Пример использования
if __name__ == "__main__":
    operations = load_operations("data/operations.json")  # Учтите, что файл теперь в папке data/

    # Выводим первую операцию для проверки
    if operations:
        first_operation = operations[0]
        print("ID операции:", first_operation["id"])
        print("Дата:", parse_date(first_operation["date"]))
        print("Сумма:", first_operation["operationAmount"]["amount"])
        print("Валюта:", first_operation["operationAmount"]["currency"]["name"])
        print("Описание:", first_operation["description"])
