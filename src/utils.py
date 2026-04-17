"""
Модуль для работы с данными транзакций.
"""

import requests
import json
import logging
import os
from typing import Any, Dict, List
from datetime import datetime
import pandas as pd

# 1. СОЗДАЕМ ОТДЕЛЬНЫЙ ОБЪЕКТ ЛОГЕРА
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# 2. СОЗДАЕМ ПАПКУ ДЛЯ ЛОГОВ
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 3. НАСТРАИВАЕМ FILE_HANDLER
file_handler = logging.FileHandler(
    filename=os.path.join(log_dir, "utils.log"), mode="w", encoding="utf-8"  # перезаписываем при каждом запуске
)
file_handler.setLevel(logging.DEBUG)

# 4. НАСТРАИВАЕМ FILE_FORMATTER
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# 5. ДОБАВЛЯЕМ HANDLER К ЛОГЕРУ
utils_logger.addHandler(file_handler)


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON-файла.
    """
    utils_logger.debug(f"Попытка загрузки файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            utils_logger.info(f"Успешно загружено {len(data)} операций из {file_path}")
            return data
        else:
            utils_logger.warning(f"Файл {file_path} содержит не список, а {type(data)}")
            return []

    except FileNotFoundError:
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        utils_logger.exception(f"Неожиданная ошибка при загрузке файла {file_path}: {e}")
        return []


def filter_operations_by_status(operations: List[Dict[str, Any]], status: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.
    """
    utils_logger.debug(f"Фильтрация операций по статусу: {status}")

    try:
        filtered = [op for op in operations if op.get("state") == status]
        utils_logger.info(f"Отфильтровано {len(filtered)} операций со статусом {status}")
        return filtered
    except Exception as e:
        utils_logger.exception(f"Ошибка при фильтрации операций: {e}")
        return []


def get_transaction_amount(transaction: Dict[str, Any]) -> float:
    """
    Получает сумму транзакции.
    """
    utils_logger.debug("Извлечение суммы из транзакции")

    try:
        amount = float(transaction.get("operationAmount", {}).get("amount", "0"))
        utils_logger.info(f"Успешно получена сумма: {amount}")
        return amount
    except (ValueError, TypeError, AttributeError) as e:
        utils_logger.error(f"Ошибка при получении суммы: {e}")
        return 0.0


def get_greeting(date_time_str: str) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Args:
        date_time_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        str: 'Доброе утро', 'Добрый день', 'Добрый вечер' или 'Доброй ночи'.
    """
    try:
        # Преобразуем строку в объект datetime
        dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        hour = dt.hour
    except ValueError:
        # Если строка некорректна, считаем, что сейчас день (можно и ошибку бросить)
        # Но для простоты предположим, что данные верные
        print(f"Ошибка: Неверный формат даты/времени '{date_time_str}'")
        return "Добрый день"

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла и возвращает DataFrame.

    Args:
        file_path: Путь к файлу.

    Returns:
        pd.DataFrame: DataFrame с транзакциями.
    """
    try:
        df = pd.read_excel(file_path)
        # Приводим названия столбцов к нижнему регистру и убираем пробелы для удобства
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        return df
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return pd.DataFrame()


def filter_transactions_by_date(df: pd.DataFrame, date_time_str: str) -> pd.DataFrame:
    """
    Фильтрует транзакции с начала месяца по указанную дату.

    Args:
        df: DataFrame с транзакциями.
        date_time_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame.
    """
    # Преобразуем строку в datetime
    target_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Получаем первый день месяца
    start_date = target_date.replace(day=1, hour=0, minute=0, second=0)

    # Преобразуем колонку 'дата_операции' в datetime
    df['дата_операции'] = pd.to_datetime(df['дата_операции'], format='%d.%m.%Y %H:%M:%S')

    # Фильтруем
    mask = (df['дата_операции'] >= start_date) & (df['дата_операции'] <= target_date)

    return df[mask].copy()


def get_cards_info(df: pd.DataFrame) -> list:
    """
    Возвращает информацию по картам: последние 4 цифры, сумма расходов, кешбэк.

    Args:
        df: DataFrame с транзакциями.

    Returns:
        list: Список словарей с данными по картам.
    """
    # Группируем по номеру карты
    cards_group = df.groupby('номер_карты').agg({
        'сумма_платежа': 'sum',
        'кэшбэк': 'sum'
    }).reset_index()

    result = []
    for _, row in cards_group.iterrows():
        # Извлекаем последние 4 цифры (удаляем звёздочку)
        last_digits = row['номер_карты'].replace('*', '')
        result.append({
            "last_digits": last_digits,
            "total_spent": round(row['сумма_платежа'], 2),
            "cashback": round(row['кэшбэк'], 2)
        })

    return result


def get_top_transactions(df: pd.DataFrame, n: int = 5) -> list:
    """
    Возвращает топ-N транзакций по сумме платежа.

    Args:
        df: DataFrame с транзакциями.
        n: Количество транзакций (по умолчанию 5).

    Returns:
        list: Список словарей с данными о транзакциях.
    """
    # Сортируем по сумме платежа (по убыванию)
    sorted_df = df.sort_values('сумма_платежа', ascending=False).head(n)

    result = []
    for _, row in sorted_df.iterrows():
        result.append({
            "date": row['дата_операции'].strftime('%d.%m.%Y'),
            "amount": round(row['сумма_платежа'], 2),
            "category": row['категория'],
            "description": row['описание']
        })

    return result


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют к рублю через API.

    Args:
        currencies: Список кодов валют (например, ['USD', 'EUR'])

    Returns:
        List[Dict[str, Any]]: Список словарей с валютами и курсами
    """
    # TODO: добавить реальный API ключ
    # Пока заглушка
    return [{"currency": curr, "rate": 0.0} for curr in currencies]


def load_user_settings(file_path: str = 'user_settings.json') -> Dict[str, Any]:
    """
    Загружает настройки пользователя из JSON-файла.

    Args:
        file_path: Путь к файлу настроек

    Returns:
        Dict[str, Any]: Словарь с настройками
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл настроек {file_path} не найден")
        return {"user_currencies": [], "user_stocks": []}
