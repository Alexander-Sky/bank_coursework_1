import json

import pandas as pd
import pytest

from src.reports import spending_by_category


def test_spending_by_category():
    """Тест расчёта трат по категории."""
    data = {
        "дата_операции": ["01.12.2021 10:00:00", "15.12.2021 12:00:00", "20.12.2021 15:00:00"],
        "категория": ["Супермаркеты", "Супермаркеты", "Кафе"],
        "сумма_платежа": [-1000, -500, -300],
    }
    df = pd.DataFrame(data)
    result = json.loads(spending_by_category(df, "Супермаркеты", "2021-12-31"))
    assert result["category"] == "Супермаркеты"
    assert result["total_spent"] == 1500.0
