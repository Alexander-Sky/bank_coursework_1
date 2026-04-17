"""
Тесты для модуля views.py (страница «Главная»).
"""

import pytest
from src.views import main_page


def test_main_page_structure():
    """Тест структуры JSON-ответа главной страницы."""
    result = main_page("2021-12-31 15:00:00")

    # Проверяем наличие всех ключей
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

    # Проверяем типы
    assert isinstance(result["greeting"], str)
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)


def test_main_page_greeting():
    """Тест приветствия в разное время суток."""
    # Утро
    result = main_page("2021-12-31 08:00:00")
    assert result["greeting"] == "Доброе утро"

    # День
    result = main_page("2021-12-31 14:00:00")
    assert result["greeting"] == "Добрый день"

    # Вечер
    result = main_page("2021-12-31 20:00:00")
    assert result["greeting"] == "Добрый вечер"

    # Ночь
    result = main_page("2021-12-31 02:00:00")
    assert result["greeting"] == "Доброй ночи"


def test_main_page_cards():
    """Тест данных по картам."""
    result = main_page("2021-12-31 15:00:00")

    for card in result["cards"]:
        assert "last_digits" in card
        assert "total_spent" in card
        assert "cashback" in card
        assert isinstance(card["last_digits"], str)
        assert isinstance(card["total_spent"], float)
        assert isinstance(card["cashback"], float)


def test_main_page_top_transactions():
    """Тест топ-5 транзакций."""
    result = main_page("2021-12-31 15:00:00")

    # Должно быть не больше 5 транзакций
    assert len(result["top_transactions"]) <= 5

    for trans in result["top_transactions"]:
        assert "date" in trans
        assert "amount" in trans
        assert "category" in trans
        assert "description" in trans
        assert isinstance(trans["date"], str)
        assert isinstance(trans["amount"], float)