"""
Тесты для модуля file_readers.
"""

import os
import tempfile
from unittest.mock import patch

import pandas as pd

from src.file_readers import read_csv_file, read_csv_with_pandas, read_excel_file


def test_read_csv_file_success():
    """Тест успешного чтения CSV файла"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("id;state;date;amount;currency_name;currency_code;from;to;description\n")
        f.write("650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 1;Счет 2;Перевод\n")
        temp_file = f.name

    try:
        transactions = read_csv_file(temp_file)
        assert len(transactions) == 1
        assert transactions[0]["id"] == "650703"
        assert transactions[0]["state"] == "EXECUTED"
    finally:
        os.unlink(temp_file)


def test_read_csv_file_not_found():
    """Тест обработки отсутствующего файла"""
    transactions = read_csv_file("non_existent_file.csv")
    assert transactions == []


def test_read_csv_file_empty():
    """Тест чтения пустого CSV файла"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("")
        temp_file = f.name

    try:
        transactions = read_csv_file(temp_file)
        assert transactions == []
    finally:
        os.unlink(temp_file)


@patch("pandas.read_excel")
def test_read_excel_file_success(mock_read_excel):
    """Тест успешного чтения Excel файла с mock"""
    test_data = pd.DataFrame(
        {
            "id": ["650703"],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210],
            "currency_name": ["Sol"],
            "currency_code": ["PEN"],
        }
    )

    mock_read_excel.return_value = test_data
    transactions = read_excel_file("test.xlsx")

    assert len(transactions) == 1
    assert transactions[0]["id"] == "650703"
    mock_read_excel.assert_called_once_with("test.xlsx")


def test_read_excel_file_not_found():
    """Тест обработки отсутствующего Excel файла"""
    transactions = read_excel_file("non_existent_file.xlsx")
    assert transactions == []


@patch("pandas.read_csv")
def test_read_csv_with_pandas_success(mock_read_csv):
    """Тест успешного чтения CSV с pandas"""
    test_data = pd.DataFrame(
        {
            "id": ["650703"],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210],
            "currency_name": ["Sol"],
            "currency_code": ["PEN"],
        }
    )

    mock_read_csv.return_value = test_data
    transactions = read_csv_with_pandas("test.csv")

    assert len(transactions) == 1
    assert transactions[0]["id"] == "650703"
    mock_read_csv.assert_called_once_with("test.csv", sep=";")


def test_read_csv_with_pandas_not_found():
    """Тест обработки отсутствующего файла в pandas версии"""
    transactions = read_csv_with_pandas("non_existent_file.csv")
    assert transactions == []
