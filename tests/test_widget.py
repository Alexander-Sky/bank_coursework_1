from src.widget import get_date, mask_account_card


def test_mask_account_card():
    test_cases = [
        ("Visa Platinum 4500123456789012", "Visa Platinum 4500 12** **** 9012"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
    ]

    for input_str, expected in test_cases:
        assert mask_account_card(input_str) == expected

    assert mask_account_card("Счет 73654108430135874305") == "Счет ** 4305"
    assert mask_account_card("Счет 40817810000000000000") == "Счет ** 0000"


def test_get_date():
    test_dates = [
        ("2023-10-01T12:00:00", "01.10.2023"),
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2022-12-31T23:59:59", "31.12.2022"),
    ]

    for input_date, expected in test_dates:
        assert get_date(input_date) == expected
