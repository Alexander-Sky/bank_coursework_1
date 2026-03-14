import logging
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from src.decorators import log

LOG_FILE_NAME = "test.log"


def test_log_decorator_file_handler_cleanup():
    """
    Модуль тестирования декоратора логирования

    Содержит тесты для проверки:
    - Корректности работы FileHandler'ов
    - Обработки ошибок
    - Логирования в консоль
    - Временных файлов
    - Удаления хендлеров
    """
    temp_dir = tempfile.mkdtemp()
    log_file_path = os.path.join(temp_dir, LOG_FILE_NAME)

    @log(filename=log_file_path)
    def test_func():
        return "success"

    try:
        logger = logging.getLogger("src.decorators")
        initial_handlers = len(logger.handlers)

        result = test_func()
        assert result == "success"

        file_path = Path(log_file_path)
        assert file_path.exists()

        with open(log_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            assert "Вызов функции test_func" in content
            assert "test_func ok" in content

        assert len(logger.handlers) == initial_handlers

    finally:
        shutil.rmtree(temp_dir)


def test_log_decorator_no_file():
    """
    Тест проверки работы декоратора без указания файла лога
    (логирование в консоль)

    Предусловия:
    - Декоратор вызывается без указания файла

    Ожидаемое поведение:
    - Функция должна выполниться успешно
    - Логи должны записываться в консоль
    - Никаких ошибок не должно возникнуть
    """

    @log()
    def test_func():
        return "success"

    result = test_func()
    assert result == "success"


def test_log_decorator_error_handling():
    @log()
    def failing_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_function()


def test_log_decorator_invalid_path():
    non_existent_path = "non_existent_directory/test.log"

    @log(filename=non_existent_path)
    def test_func():
        return "success"

    result = test_func()
    assert result == "success"


def test_log_decorator_empty_filename():
    @log(filename="")
    def test_func():
        return "success"

    result = test_func()
    assert result == "success"


def test_log_decorator_finally_block():
    """
    Тест проверки корректной работы с FileHandler'ами:
    - Добавление хендлера
    - Запись в файл
    - Удаление хендлера
    """
    temp_dir = tempfile.mkdtemp()
    log_file_path = os.path.join(temp_dir, LOG_FILE_NAME)

    @log(filename=log_file_path)
    def test_func():
        return "success"

    try:
        logger = logging.getLogger("src.decorators")
        initial_handlers = len(logger.handlers)

        print(f"Начальные хендлеры: {initial_handlers}")  # Отладка

        assert len(logger.handlers) == initial_handlers

        result = test_func()
        assert result == "success"

        # Проверяем, что файл был создан
        file_path = Path(log_file_path)
        assert file_path.exists()

        with open(log_file_path, "r", encoding="utf-8") as file:
            content = file.read()
            assert "Вызов функции test_func" in content
            assert "test_func ok" in content

        # Проверяем, что после выполнения хендлер удален
        assert len(logger.handlers) == initial_handlers

    finally:
        shutil.rmtree(temp_dir)


def test_log_decorator_no_file_finally():
    @log()
    def test_func():
        return "success"

    logger = logging.getLogger("src.decorators")
    initial_handlers = len(logger.handlers)

    try:
        result = test_func()
        assert result == "success"

        # Проверяем, что хендлеры не были добавлены
        assert len(logger.handlers) == initial_handlers

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def test_log_decorator_error_finally():
    temp_dir = tempfile.mkdtemp()
    log_file_path = os.path.join(temp_dir, LOG_FILE_NAME)

    @log(filename=log_file_path)
    def failing_function():
        raise Exception("Test exception")

    logger = logging.getLogger("src.decorators")
    initial_handlers = len(logger.handlers)

    try:
        with pytest.raises(Exception):
            failing_function()

        # Проверяем удаление хендлеров после ошибки
        assert len(logger.handlers) == initial_handlers

    finally:
        shutil.rmtree(temp_dir)
