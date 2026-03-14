from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте

    :param transactions: список словарей с транзакциями
    :param currency: код валюты для фильтрации
    :return: итератор с отфильтрованными транзакциями
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction
            print(f"Found transaction with currency {currency}")  # Для отладки


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Возвращает описания транзакций

    :param transactions: список словарей с транзакциями
    :return: итератор с описаниями
    """
    for transaction in transactions:
        yield transaction.get("description", "Нет описания")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера карт в заданном диапазоне

    :param start: начальное значение
    :param stop: конечное значение
    :return: отформатированные номера карт
    """
    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:]}"
