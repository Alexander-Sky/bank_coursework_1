import os

import pandas as pd

from src.utils import (
    filter_operations_by_status,
    filter_transactions_by_date,
    get_cards_info,
    get_currency_rates,
    get_greeting,
    get_top_transactions,
    load_transactions,
    load_user_settings,
)


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


def test_get_greeting():
    """Тест определения времени суток."""
    assert get_greeting("2021-12-31 08:00:00") == "Доброе утро"
    assert get_greeting("2021-12-31 14:00:00") == "Добрый день"
    assert get_greeting("2021-12-31 20:00:00") == "Добрый вечер"
    assert get_greeting("2021-12-31 02:00:00") == "Доброй ночи"


def test_load_transactions():
    """Тест загрузки Excel-файла."""
    df = load_transactions("data/operations.xlsx")
    assert df is not None
    assert not df.empty


def test_filter_transactions_by_date():
    """Тест фильтрации по дате."""
    df = load_transactions("data/operations.xlsx")
    filtered = filter_transactions_by_date(df, "2021-12-31 15:00:00")
    assert filtered is not None
    # Проверяем, что все даты в отфильтрованном диапазоне
    if not filtered.empty:
        min_date = filtered["дата_операции"].min()
        max_date = filtered["дата_операции"].max()
        assert min_date >= pd.Timestamp("2021-12-01")
        assert max_date <= pd.Timestamp("2021-12-31 23:59:59")


def test_get_cards_info():
    """Тест получения данных по картам."""
    df = load_transactions("data/operations.xlsx")
    filtered = filter_transactions_by_date(df, "2021-12-31 15:00:00")
    cards = get_cards_info(filtered)

    assert isinstance(cards, list)
    for card in cards:
        assert "last_digits" in card
        assert "total_spent" in card
        assert "cashback" in card


def test_get_top_transactions():
    """Тест получения топ-транзакций."""
    df = load_transactions("data/operations.xlsx")
    filtered = filter_transactions_by_date(df, "2021-12-31 15:00:00")
    top = get_top_transactions(filtered, 5)

    assert isinstance(top, list)
    assert len(top) <= 5
    for trans in top:
        assert "date" in trans
        assert "amount" in trans
        assert "category" in trans
        assert "description" in trans


def test_get_currency_rates_empty():
    """Тест получения курсов для пустого списка."""
    rates = get_currency_rates([])
    assert rates == []


def test_filter_transactions_by_date_empty_df():
    """Тест фильтрации пустого DataFrame."""
    # Создаём пустой DataFrame с правильными колонками
    empty_df = pd.DataFrame(columns=["дата_операции"])
    filtered = filter_transactions_by_date(empty_df, "2021-12-31 15:00:00")
    assert filtered.empty


def test_get_currency_rates_no_api_key():
    """Тест получения курсов при отсутствии API ключа."""
    # Сохраняем оригинальный API_KEY
    import src.utils

    original_key = src.utils.API_KEY
    src.utils.API_KEY = None

    try:
        rates = get_currency_rates(["USD"])
        assert len(rates) == 1
        assert rates[0]["currency"] == "USD"
        assert rates[0]["rate"] == 0.0
    finally:
        # Восстанавливаем ключ
        src.utils.API_KEY = original_key


def test_load_user_settings_invalid_json():
    """Тест загрузки настроек с некорректным JSON."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        f.write("{invalid json}")
        temp_file = f.name

    try:
        settings = load_user_settings(temp_file)
        assert "user_currencies" in settings
        assert "user_stocks" in settings
    finally:
        os.unlink(temp_file)
