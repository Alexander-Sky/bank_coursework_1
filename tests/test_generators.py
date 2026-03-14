import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2023-10-01T12:00:00",
            "operationAmount": {
                "amount": "5000.00",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 12345678901234567890",
            "to": "Счет 98765432109876543210",
        },
        {
            "id": 987654321,
            "state": "EXECUTED",
            "date": "2023-10-02T12:00:00",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод физическому лицу",
            "from": "Счет 11111111111111111111",
            "to": "Счет 22222222222222222222",
        },
    ]


def test_filter_by_currency(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    # Проверяем, что хотя бы одна транзакция найдена
    assert len(list(usd_transactions)) >= 1


def test_transaction_descriptions(transactions):
    descriptions = transaction_descriptions(transactions)
    expected = [transaction["description"] for transaction in transactions]
    assert list(descriptions) == expected


@pytest.mark.parametrize(
    "start,stop,expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        )
    ],
)
def test_card_number_generator(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected
