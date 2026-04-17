from typing import Dict, Any
from src.utils import load_transactions, filter_transactions_by_date, get_greeting
from src.utils import get_cards_info, get_top_transactions


def main_page(date_time_str: str) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для главной страницы.

    Args:
        date_time_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Dict[str, Any]: Словарь с данными для JSON-ответа.
    """
    # 1. Загружаем данные
    df = load_transactions('data/operations.xlsx')
    if df.empty:
        return {"error": "Не удалось загрузить данные"}

    # 2. Фильтруем по дате (с начала месяца)
    filtered_df = filter_transactions_by_date(df, date_time_str)

    # 3. Получаем приветствие
    greeting = get_greeting(date_time_str)

    # 4. Получаем данные по картам
    cards = get_cards_info(filtered_df)

    # 5. Получаем топ-5 транзакций
    top_transactions = get_top_transactions(filtered_df, 5)

    # 6. Возвращаем результат
    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": [],  # Пока заглушка
        "stock_prices": []  # Пока заглушка
    }