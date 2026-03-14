import os

from src.utils import filter_operations_by_status, load_operations


def test_load_operations():
    # Проверяем загрузку существующего файла
    operations = load_operations("data/operations.json")
    assert isinstance(operations, list)
    assert len(operations) > 0

    # Проверяем обработку пустого файла
    with open("data/empty.json", "w") as f:
        f.write("[]")
    empty_operations = load_operations("data/empty.json")
    assert empty_operations == []
    os.remove("data/empty.json")

    # Проверяем обработку не-list содержимого
    with open("data/invalid.json", "w") as f:
        f.write("{}")
    invalid_operations = load_operations("data/invalid.json")
    assert invalid_operations == []
    os.remove("data/invalid.json")

    # Проверяем обработку отсутствующего файла
    non_existent_operations = load_operations("non_existent_file.json")
    assert non_existent_operations == []


def test_filter_operations_by_status():
    """Тест для функции фильтрации операций по статусу."""
    test_operations = [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "PENDING", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "CANCELED", "amount": 400},
    ]

    # Тест с фильтрацией по умолчанию (EXECUTED)
    executed = filter_operations_by_status(test_operations)
    assert len(executed) == 2
    assert all(op["state"] == "EXECUTED" for op in executed)

    # Тест с фильтрацией по PENDING
    pending = filter_operations_by_status(test_operations, "PENDING")
    assert len(pending) == 1
    assert pending[0]["state"] == "PENDING"

    # Тест с фильтрацией по несуществующему статусу
    none_status = filter_operations_by_status(test_operations, "NON_EXISTENT")
    assert len(none_status) == 0

    # Тест с пустым списком
    empty_result = filter_operations_by_status([])
    assert empty_result == []
