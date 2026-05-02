# Bank Coursework — Приложение для анализа банковских операций

## Описание проекта

Приложение для анализа банковских транзакций из Excel-файла. Генерирует JSON-данные для веб-страниц, предоставляет сервисы для анализа кешбэка, поиска транзакций и формирования отчётов. Реализована обработка исключений для корректной работы с данными.

## Реализованная функциональность

### Веб-страницы
- **Главная** — приветствие, карты, топ-5 транзакций, курсы валют

### Сервисы
- **Простой поиск** — поиск транзакций по строке в описании или категории

### Отчёты
- **Траты по категории** — сумма трат за последние 3 месяца

### Обработка исключений (17.1)
- Класс Product — выбрасывает `ValueError` при попытке создать товар с нулевым количеством
- Класс Category — метод `middle_price` корректно обрабатывает пустую категорию (возвращает 0)
- Округление средней цены до 2 знаков после запятой

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

# Установка зависимостей
poetry install

# Активация окружения
poetry shell

# Запуск демонстрационного скрипта
poetry run python main.py

# Запуск всех тестов
poetry run pytest

# Проверка покрытия
poetry run pytest --cov=src --cov-report=term-missing

# Проверка качества кода
poetry run flake8
poetry run mypy src
Структура проекта

bank_coursework_1/
├── data/
│   └── operations.xlsx          # Excel-файл с транзакциями
├── src/
│   ├── product.py               # Класс Product (товар)
│   ├── category.py              # Класс Category (категория)
│   ├── utils.py                 # Вспомогательные функции
│   ├── views.py                 # Функции для веб-страниц
│   ├── reports.py               # Функции для отчётов
│   └── services.py              # Функции для сервисов
├── tests/
│   ├── test_product.py          # Тесты для Product
│   ├── test_category.py         # Тесты для Category
│   ├── test_exceptions.py       # Тесты для исключений
│   └── ...                      # Остальные тесты
├── user_settings.json           # Настройки пользователя
├── .env                         # Переменные окружения
├── main.py                      # Демонстрационный скрипт
├── pyproject.toml               # Конфигурация Poetry
└── README.md

# Покрытие тестами


Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\__init__.py                0      0   100%
src\category.py               13      0   100%
src\decorators.py             32      0   100%
src\external_api.py           61      9    85%   54, 57-60, 73, 75, 78, 110
src\file_readers.py           52     11    79%   27, 52, 58-60, 81-83, 104-106
src\generators.py             13      0   100%
src\masks.py                  39      0   100%
src\operations_parser.py      23      9    61%   24, 29-38
src\processing.py              5      0   100%
src\product.py                 8      0   100%
src\utils.py                  50     17    66%   52-57, 70-72, 79-87
src\widget.py                 18      2    89%   44-46
--------------------------------------------------------
TOTAL                        314     48    85%

Coverage HTML written to dir htmlcov

# Пример использования
Создание товара с обработкой исключения
python
from src.product import Product

try:
    product = Product("Смартфон", "Флагман", 100000.0, 0)
except ValueError as e:
    print(f"Ошибка: {e}")  # Товар с нулевым количеством не может быть добавлен
Подсчёт средней цены в категории
python
from src.category import Category
from src.product import Product

products = [Product("A", "desc", 100.0, 1), Product("B", "desc", 200.0, 1)]
category = Category("Тест", "Описание", products)
print(category.middle_price())  # 150.0

empty_category = Category("Пустая", "Описание", [])
print(empty_category.middle_price())  # 0.0

# Статус проекта

- Страница «Главная» — реализована

- Сервис «Простой поиск» — реализован

- Отчёт «Траты по категории» — реализован

- Обработка исключений — реализована


Контакты
Автор: Alexander Schischkin