import os

from src.operations_parser import load_operations


def test_load_operations_valid_file():
    operations = load_operations("data/operations.json")
    assert isinstance(operations, list)
    assert len(operations) > 0


def test_load_operations_empty_file():
    # Создаем временный пустой файл для теста
    with open("data/empty.json", "w") as f:
        f.write("[]")
    operations = load_operations("data/empty.json")
    assert operations == []
    os.remove("data/empty.json")


def test_load_operations_non_list():
    # Создаем файл с не-list содержимым
    with open("data/invalid.json", "w") as f:
        f.write("{}")
    operations = load_operations("data/invalid.json")
    assert operations == []  # Ожидаем пустой список
    os.remove("data/invalid.json")


def test_load_operations_file_not_found():
    # Проверяем, что при отсутствии файла возвращается пустой список
    operations = load_operations("non_existent_file.json")
    assert operations == []


# Или альтернативный вариант с обработкой исключения в функции
def test_load_operations_file_not_found_alt():
    operations = load_operations("non_existent_file.json")
    assert operations == []  # Если функция должна возвращать пустой список
