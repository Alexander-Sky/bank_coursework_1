from typing import Any, Dict

from src.utils import (
    filter_transactions_by_date,
    get_cards_info,
    get_currency_rates,
    get_greeting,
    get_top_transactions,
    load_transactions,
    load_user_settings,
)


def main_page(date_time_str: str) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для главной страницы.

    Args:
        date_time_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Dict[str, Any]: Словарь с данными для JSON-ответа.
    """
    # 1. Загружаем данные
    df = load_transactions("data/operations.xlsx")
    if df.empty:
        return {"error": "Не удалось загрузить данные"}

    # 2. Фильтруем по дате
    filtered_df = filter_transactions_by_date(df, date_time_str)

    # 3. Получаем приветствие
    greeting = get_greeting(date_time_str)

    # 4. Получаем данные по картам
    cards = get_cards_info(filtered_df)

    # 5. Получаем топ-5 транзакций
    top_transactions = get_top_transactions(filtered_df, 5)

    # --- НОВАЯ ЧАСТЬ: загружаем настройки и получаем курсы ---
    settings = load_user_settings("user_settings.json")
    currency_rates = get_currency_rates(settings.get("user_currencies", []))
    # Пока оставляем stock_prices пустым, это для следующего шага
    stock_prices: list[dict] = []

    # 6. Возвращаем результат
    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,  # <-- теперь здесь реальные курсы
        "stock_prices": stock_prices,
    }
