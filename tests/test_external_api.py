"""
Тесты для модуля external_api.
"""

import os
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from src.external_api import convert_to_rub, get_exchange_rates

# Тестовые данные
TRANSACTION_RUB = {
    "operationAmount": {
        "amount": "31957.58",
        "currency": {"name": "руб.", "code": "RUB"},
    }
}

TRANSACTION_USD = {
    "operationAmount": {
        "amount": "8221.37",
        "currency": {"name": "USD", "code": "USD"},
    }
}


@pytest.mark.parametrize(
    "set_vars,missing_env,expected_error",
    [
        # Случаи с отсутствующей API_URL
        (
            {"API_KEY": "test_key"},
            {"API_URL": None},
            "Не настроены переменные окружения: API_URL",
        ),
        (
            {"API_KEY": "test_key"},
            {"API_URL": ""},
            "Не настроены переменные окружения: API_URL",
        ),
        # Случаи с отсутствующей API_KEY
        (
            {"API_URL": "https://example.com"},
            {"API_KEY": None},
            "Не настроены переменные окружения: API_KEY",
        ),
        (
            {"API_URL": "https://example.com"},
            {"API_KEY": ""},
            "Не настроены переменные окружения: API_KEY",
        ),
    ],
)
def test_missing_environment_variables(set_vars, missing_env, expected_error):
    """
    Тест проверяет реакцию на отсутствие переменных окружения.
    """
    with patch.dict("os.environ", {}, clear=True):
        # Устанавливаем переменные, которые должны быть
        for key, value in set_vars.items():
            os.environ[key] = value

        # Устанавливаем/удаляем тестируемую переменную
        for key, value in missing_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

        # Проверяем, что вызывается правильное исключение
        with pytest.raises(ValueError, match=expected_error):
            get_exchange_rates()


@patch("requests.get")
def test_network_errors(mock_get):
    """
    Тест обработки сетевых ошибок.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        network_errors = [ConnectionError, Timeout, HTTPError, RequestException]

        for error in network_errors:
            mock_get.side_effect = error
            result = convert_to_rub(TRANSACTION_USD)
            assert result == 8221.37


@patch("requests.get")
def test_convert_rub(mock_get):
    """
    Тест конвертации рублей (должен вернуть ту же сумму).
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"success": True, "result": 31957.58}
        mock_response.raise_for_status.return_value = None

        result = convert_to_rub(TRANSACTION_RUB)
        assert result == 31957.58


@patch("requests.get")
def test_convert_usd(mock_get):
    """
    Тест конвертации долларов в рубли.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        mock_response = mock_get.return_value
        expected = 8221.37 * 78.25
        mock_response.json.return_value = {
            "success": True,
            "result": expected,
            "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
            "info": {"rate": 78.25},
        }
        mock_response.raise_for_status.return_value = None

        result = convert_to_rub(TRANSACTION_USD)
        assert isinstance(result, float)
        assert result == pytest.approx(expected)


def test_invalid_amount():
    """
    Тест обработки некорректной суммы.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        invalid_transaction = {
            "operationAmount": {
                "amount": "abc",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        with pytest.raises(ValueError, match="Некорректные данные операции"):
            convert_to_rub(invalid_transaction)


def test_unknown_currency():
    """
    Тест обработки неизвестной валюты.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        unknown_currency_transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"name": "GBP", "code": "GBP"},
            }
        }

        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.json.return_value = {
                "success": False,
                "error": "Currency not found",
            }
            mock_response.raise_for_status.return_value = None

            result = convert_to_rub(unknown_currency_transaction)
            assert result == 100.0


def test_zero_amount_conversion():
    """
    Тест конвертации нулевой суммы.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        transaction = {"operationAmount": {"amount": "0", "currency": {"code": "USD"}}}

        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.json.return_value = {"success": True, "result": 0.0}
            mock_response.raise_for_status.return_value = None

            result = convert_to_rub(transaction)
            assert result == 0.0


def test_get_exchange_rates_success():
    """
    Тест успешного получения курсов.
    """
    with patch.dict(
        "os.environ",
        {"API_KEY": "test_key", "API_URL": "https://example.com"},
        clear=True,
    ):
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.json.return_value = {
                "success": True,
                "rates": {"RUB": 78.25, "EUR": 0.92},
            }
            mock_response.raise_for_status.return_value = None

            rates = get_exchange_rates()
            assert rates is not None
            assert rates["RUB"] == 78.25
