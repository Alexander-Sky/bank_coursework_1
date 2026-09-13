

### Веб-страницы
- **Главная** — приветствие, карты, топ-5 транзакций, курсы валют

### Сервисы
- **Простой поиск** — поиск транзакций по строке в описании или категории

### Отчёты
- **Траты по категории** — сумма трат за последние 3 месяца



## Технологии

- Python 3.14
- Poetry — управление зависимостями
- pandas — работа с Excel-данными
- requests — запросы к API
- pytest — тестирование
- flake8, black, isort, mypy — контроль качества кода

## Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/Alexander-Sky/bank_coursework_1.git
cd bank_coursework_1


python
from src.category import Category
from src.product import Product

products = [Product("A", "desc", 100.0, 1), Product("B", "desc", 200.0, 1)]
category = Category("Тест", "Описание", products)
print(category.middle_price())  # 150.0


# Статус проекта

- Страница «Главная» — реализована

- Сервис «Простой поиск» — реализован

- Отчёт «Траты по категории» — реализован

- Обработка исключений — реализована


Контакты
Автор: Alexander Schischkin