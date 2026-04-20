"""
Модуль для генерации отчетов (траты по категориям, дням недели и т.д.).
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import pandas as pd

# Настройка логгера
logger = logging.getLogger(__name__)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """
    Рассчитывает траты по заданной категории за последние 3 месяца (от переданной даты).

    Args:
        transactions: DataFrame с транзакциями.
        category: Название категории для анализа.
        date: Опциональная дата в формате 'YYYY-MM-DD'. Если не указана, используется текущая дата.

    Returns:
        str: JSON-строка с суммой трат по категории.
    """
    if transactions.empty:
        logger.warning("Получен пустой DataFrame")
        return json.dumps({"category": category, "total_spent": 0.0}, ensure_ascii=False)

    # Определяем целевую дату
    if date:
        target_date = pd.to_datetime(date)
    else:
        target_date = pd.Timestamp.now()

    # Рассчитываем дату начала периода (3 месяца назад)
    start_date = target_date - timedelta(days=90)

    # Преобразуем даты в нужный формат, если необходимо
    if 'дата_операции' in transactions.columns:
        transactions['дата_операции'] = pd.to_datetime(transactions['дата_операции'], format='%d.%m.%Y %H:%M:%S')

        # Фильтруем DataFrame по диапазону дат
        mask = (transactions['дата_операции'] >= start_date) & (transactions['дата_операции'] <= target_date)
        filtered_df = transactions[mask]
    else:
        logger.error("В DataFrame нет колонки 'дата_операции'")
        filtered_df = transactions

    # Фильтруем по категории и считаем сумму трат (отрицательные суммы)
    category_mask = filtered_df['категория'].str.lower() == category.lower()
    expenses = filtered_df[category_mask & (filtered_df['сумма_платежа'] < 0)]['сумма_платежа'].sum()

    result = {
        "category": category,
        "total_spent": abs(round(expenses, 2))
    }
    logger.info(f"Траты по категории '{category}' за последние 3 месяца: {result['total_spent']}")
    return json.dumps(result, ensure_ascii=False, indent=2)