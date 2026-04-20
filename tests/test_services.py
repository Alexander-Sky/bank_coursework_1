import json

import pytest

from src.services import search_transactions


def test_search_transactions_found():
    """Тест поиска существующей строки."""
    data = [
        {"описание": "Покупка в магазине", "категория": "Супермаркеты"},
        {"описание": "Оплата связи", "категория": "Связь"},
    ]
    result = json.loads(search_transactions(data, "магазин"))
    assert len(result) == 1
    assert result[0]["категория"] == "Супермаркеты"


def test_search_transactions_not_found():
    """Тест поиска несуществующей строки."""
    data = [{"описание": "Покупка", "категория": "Супермаркеты"}]
    result = json.loads(search_transactions(data, "ресторан"))
    assert result == []


def test_search_transactions_empty_query():
    """Тест с пустым запросом."""
    data = [{"описание": "Покупка"}]
    result = json.loads(search_transactions(data, ""))
    assert result == []
