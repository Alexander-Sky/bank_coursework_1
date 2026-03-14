"""
Модуль для маскировки банковских карт и счетов.
"""

import logging
import os
from typing import Union

# 1. СОЗДАЕМ ОТДЕЛЬНЫЙ ОБЪЕКТ ЛОГЕРА
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# 2. СОЗДАЕМ ПАПКУ ДЛЯ ЛОГОВ
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 3. НАСТРАИВАЕМ FILE_HANDLER
file_handler = logging.FileHandler(
    filename=os.path.join(log_dir, "masks.log"), mode="w", encoding="utf-8"  # перезаписываем при каждом запуске
)
file_handler.setLevel(logging.DEBUG)

# 4. НАСТРАИВАЕМ FILE_FORMATTER
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# 5. ДОБАВЛЯЕМ HANDLER К ЛОГЕРУ
masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """
    Маскирует номер банковской карты.
    """
    masks_logger.debug(f"Начало маскировки номера карты: {str(card_number)[:4]}...")

    try:
        card_str = str(card_number).replace(" ", "")

        if len(card_str) != 16 or not card_str.isdigit():
            masks_logger.error(f"Неверный формат номера карты: {card_str}")
            raise ValueError("Номер карты должен содержать 16 цифр")

        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер карты: {masked}")
        return masked

    except Exception as e:
        masks_logger.exception(f"Ошибка при маскировке карты: {e}")
        raise


def get_mask_account(account_number: Union[int, str]) -> str:
    """
    Маскирует номер банковского счета.
    """
    masks_logger.debug(f"Начало маскировки номера счета: ...{str(account_number)[-4:]}")

    try:
        account_str = str(account_number).replace(" ", "")

        if len(account_str) < 4:
            masks_logger.error(f"Неверный формат номера счета: {account_str}")
            raise ValueError("Номер счета должен содержать минимум 4 символа")

        masked = f"** {account_str[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер счета: {masked}")
        return masked

    except Exception as e:
        masks_logger.exception(f"Ошибка при маскировке счета: {e}")
        raise


__all__ = ["get_mask_card_number", "get_mask_account"]
