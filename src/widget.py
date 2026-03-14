from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета.

    Args:
        input_string: строка вида "Visa 1234567890123456" или "Счет 1234567890"

    Returns:
        str: замаскированная строка
    """
    parts = input_string.split()

    if input_string.lower().startswith("счет"):
        # Для счета используем get_mask_account
        account_number = parts[-1]
        masked = get_mask_account(account_number)
        return f"Счет {masked}"
    else:
        # Для карты используем get_mask_card_number
        card_type = " ".join(parts[:-1])
        card_number = parts[-1]
        masked = get_mask_card_number(card_number)
        return f"{card_type} {masked}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string: строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: дата в формате "11.03.2024"
    """
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # Если не получилось распарсить, возвращаем как есть
        return date_string[:10].replace("-", ".")
