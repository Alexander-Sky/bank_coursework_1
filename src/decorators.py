import logging
import os
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для добавления логирования к функциям.

    Параметры:
    filename (Optional[str]): Путь к файлу для записи логов.
        Если указан, логи будут записываться в файл.
        Если не указан, логи будут выводиться в консоль.

    Функциональность:
    - Автоматическое логирование вызова функции
    - Логирование успешного выполнения
    - Обработка исключений с логированием ошибок
    - Управление FileHandler'ами для временных файлов

    Пример использования:
    @log('app.log')
    def my_function():
        return "success"
    """

    def decorator(func: Callable) -> Callable:
        logger = logging.getLogger("src.decorators")  # Используем тот же логгер

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            file_handler = None

            try:
                if filename:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

                    file_handler = logging.FileHandler(filename, encoding="utf-8")
                    formatter = logging.Formatter("%(asctime)s - %(message)s")
                    file_handler.setFormatter(formatter)

                    logger.addHandler(file_handler)
                    logger.setLevel(logging.INFO)

                    print(f"Добавлен хендлер: {file_handler}")  # Отладка

                logger.info(f"Вызов функции {func.__name__}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result

            except Exception as e:
                logger.error(f"{func.__name__} error: {str(e)}. " f"Inputs: {args}, {kwargs}")
                raise
            finally:
                if file_handler:
                    logger.removeHandler(file_handler)
                    file_handler.close()
                    print(f"Удален хендлер: {file_handler}")  # Отладка

        return wrapper

    return decorator
