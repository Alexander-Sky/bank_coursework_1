"""
Модуль для чтения финансовых транзакций из CSV и Excel файлов.
"""

import csv
from typing import Any, Dict, List

import pandas as pd


def _clean_transactions(transactions: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
    """
    Преобразует транзакции из формата pandas в нужный формат.

    Args:
        transactions: Список словарей от pandas

    Returns:
        List[Dict[str, Any]]: Очищенный список транзакций
    """
    cleaned = []
    for trans in transactions:
        cleaned_trans: Dict[str, Any] = {}
        for key, value in trans.items():
            str_key = str(key) if key is not None else ""
            if pd.isna(value):
                cleaned_trans[str_key] = None
            else:
                cleaned_trans[str_key] = value
        cleaned.append(cleaned_trans)
    return cleaned


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список в случае ошибки
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            transactions = list(reader)

            for transaction in transactions:
                for key, value in transaction.items():
                    if value == "":
                        transaction[key] = None

            return transactions
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список в случае ошибки
    """
    try:
        df = pd.read_excel(file_path)
        records = df.to_dict("records")
        return _clean_transactions(records)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []


def read_csv_with_pandas(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл с помощью pandas (альтернативный метод).

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список в случае ошибки
    """
    try:
        df = pd.read_csv(file_path, sep=";")
        records = df.to_dict("records")
        return _clean_transactions(records)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла с pandas: {e}")
        return []
