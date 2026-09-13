import pytest

from src.category import Category
from src.product import Product


def test_product_zero_quantity_exception():
    """Тест проверяет, что при создании продукта с quantity=0 выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Бракованный товар", "Неверное количество", 1000.0, 0)


def test_product_valid_quantity():
    """Тест проверяет, что продукт с положительным количеством создаётся."""
    # Проверяем, что продукт создаётся без ошибок
    product = Product("Нормальный товар", "Нормальное описание", 500.0, 10)
    assert product.name == "Нормальный товар"
    assert product.quantity == 10


def test_category_middle_price():
    """Тест проверяет подсчёт средней цены в категории с товарами."""
    product1 = Product("A", "A desc", 100.0, 1)
    product2 = Product("B", "B desc", 200.0, 1)
    category = Category("Тестовая категория", "Описание", [product1, product2])
    assert category.middle_price() == 150.0


def test_category_middle_price_empty():
    """Тест проверяет, что метод middle_price возвращает 0 для пустой категории."""
    category = Category("Пустая категория", "Описание", [])
    assert category.middle_price() == 0.0


def test_existing_tests_still_pass():
    """Тест проверяет, что старые тесты (инициализация продукта) всё ещё проходят."""
    # Это пример. Важно, чтобы все старые тесты из test_product.py и test_category.py прошли.
    product = Product("Старый тест", "Описание", 10.0, 5)
    assert product.price == 10.0
