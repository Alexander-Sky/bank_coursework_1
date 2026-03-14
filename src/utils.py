"""
Модуль для работы с данными транзакций.
"""

import json
import logging
import os
from typing import Any, Dict, List

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
