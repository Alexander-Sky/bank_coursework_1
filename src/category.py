"""
Модуль с классом Category (Категория).
"""

from typing import List
from src.product import Product


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    products: List[Product]

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.products = products

    def middle_price(self) -> float:
        """
        Вычисляет среднюю цену всех товаров в категории.
        Возвращает 0, если в категории нет товаров.
        """
        try:
            total_price = sum(product.price for product in self.products)
            return total_price / len(self.products)
        except ZeroDivisionError:
            return 0.0