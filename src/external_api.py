"""
Модуль для работы с внешним API конвертации валют.
"""

import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют от внешнего API.

    Returns:
        Optional[Dict]: Словарь с курсами валют или None в случае ошибки.

    Raises:
        ValueError: Если не настроены переменные окружения.
    """
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    # Проверяем обе переменные сразу
    missing_vars = []
    if not api_url:
        missing_vars.append("API_URL")
    if not api_key:
        missing_vars.append("API_KEY")

    if missing_vars:
        raise ValueError(f"Не настроены переменные окружения: {', '.join(missing_vars)}")

    # Для mypy: гарантируем, что api_url и api_key не None
    assert api_url is not None, "API_URL не должен быть None"
    assert api_key is not None, "API_KEY не должен быть None"

    try:
        response = requests.get(
            f"{api_url}/latest",  # Добавляем /latest
            params={"apikey": api_key, "base": "USD", "symbols": "RUB"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            rates = data.get("rates")
            if rates is None:
                return {}
            if isinstance(rates, dict):
                return rates
            return {}
        return None
    except requests.RequestException:
        return None


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    # Проверяем переменные окружения
    missing_vars = []
    if not api_url:
        missing_vars.append("API_URL")
    if not api_key:
        missing_vars.append("API_KEY")

    if missing_vars:
        raise ValueError(f"Не настроены переменные окружения: {', '.join(missing_vars)}")

    # Извлекаем данные транзакции
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("Некорректные данные операции") from exc

    # Если валюта уже рубли, возвращаем исходную сумму
    if currency_code == "RUB":
        return amount

    # Конвертируем через API - ПРАВИЛЬНЫЙ URL
    try:
        # Формируем URL для конвертации (пример из документации)
        # https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100
        convert_url = f"{api_url}/convert"

        response = requests.get(
            convert_url,
            params={"to": "RUB", "from": currency_code, "amount": amount},
            headers={"apikey": api_key},  # API ключ в headers, как требует документация
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            result = data.get("result")
            if result is not None:
                return float(result)
            return amount
        return amount
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return amount
