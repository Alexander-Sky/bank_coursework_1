"""
Модуль для сервисов (поиск, кешбэк, инвесткопилка).
"""

import json
import logging
from typing import Any, Dict, List

# Настройка логгера
logger = logging.getLogger(__name__)


def search_transactions(transactions: List[Dict[str, Any]], query: str) -> str:
    """
    Выполняет поиск транзакций по строке запроса в описании или категории.

    Args:
        transactions: Список словарей с транзакциями.
        query: Строка для поиска.

    Returns:
        str: JSON-строка со списком найденных транзакций.
    """
    logger.info(f"Поиск транзакций по запросу: '{query}'")
    if not query:
        logger.warning("Пустой поисковый запрос")
        return json.dumps([], ensure_ascii=False)

    result = []
    for trans in transactions:
        description = trans.get("описание", "").lower()
        category = trans.get("категория", "").lower()
        if query.lower() in description or query.lower() in category:
            result.append(trans)

    logger.info(f"Найдено транзакций: {len(result)}")
    return json.dumps(result, ensure_ascii=False, indent=2)
