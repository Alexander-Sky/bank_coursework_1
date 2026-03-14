import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тесты для card_number
def test_card_number_valid():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_card_number_invalid_length():
    with pytest.raises(ValueError):
        get_mask_card_number("123456789012345")  # 15 цифр вместо 16
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567")  # 17 цифр


# Тесты для account_number
def test_account_number_valid():
    assert get_mask_account("1234567890") == "** 7890"
    assert get_mask_account("ABCD1234") == "** 1234"


def test_account_number_invalid_length():
    with pytest.raises(ValueError):
        get_mask_account("123")  # меньше 4 символов
    with pytest.raises(ValueError):
        get_mask_account("")  # пустая строка


# Параметризованные тесты
@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("4500123456789012", "4500 12** **** 9012"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("7000792289606361", "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("40817810000000000000", "** 0000"),
        ("12345678901234567890", "** 7890"),
        ("abcd1234abcd1234", "** 1234"),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected
