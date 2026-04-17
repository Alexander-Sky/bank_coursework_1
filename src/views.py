import json
from typing import Dict, Any
import pandas as pd
from src.utils import load_transactions, get_greeting, get_cards_info, get_top_transactions
from src.utils import get_currency_rates, get_stock_prices

def main_page(date_time_str: str) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для главной страницы.

    Args:
        date_time_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Dict[str, Any]: Словарь с данными для JSON-ответа.
    """
    # 1. Загружаем данные из Excel
    df = load_transactions('data/operations.xlsx')

    # 2. Получаем приветствие
    greeting = get_greeting(date_time_str)

    # 3. Получаем данные по картам
    cards = get_cards_info(df, date_time_str)

    # 4. Получаем топ-5 транзакций
    top_transactions = get_top_transactions(df, date_time_str, 5)

    # 5. Получаем курсы валют (из файла настроек)
    #    user_settings = load_user_settings('user_settings.json')
    #    currency_rates = get_currency_rates(user_settings['user_currencies'])

    # 6. Получаем цены акций
    #    stock_prices = get_stock_prices(user_settings['user_stocks'])

    # 7. Собираем результат в словарь
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": [],  # Пока заглушка
        "stock_prices": []     # Пока заглушка
    }

    return result