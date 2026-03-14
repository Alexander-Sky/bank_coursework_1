from datetime import datetime
from typing import Dict, List

import pytest


@pytest.fixture
def sample_operations() -> List[Dict]:
    return [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": datetime(2019, 7, 3, 18, 35, 29),
            "description": "Перевод с карты на карту",
            "operation_id": 56789,
            "amount": {"amount": 10000, "currency": "RUB"},
        }
    ]


@pytest.fixture
def card_numbers() -> List[str]:
    return ["4500123456789012", "1234567812345678", "7000792289606361"]


@pytest.fixture
def account_numbers() -> List[str]:
    return ["40817810000000000000", "12345678901234567890", "abcd1234abcd1234"]
