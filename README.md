# Bank Coursework 1 — Приложение для анализа банковских операций
## Описание проекта

Приложение для анализа банковских транзакций из Excel-файла. Генерирует JSON-данные для веб-страниц,
предоставляет сервисы для анализа кешбэка, поиска транзакций и формирования отчётов.

## Реализованная функциональность (выбрана задача "Главная")

### Страница «Главная»

Функция `main_page` в модуле `views.py` принимает дату и время и возвращает JSON-ответ со следующими данными:

| Поле | Описание |
|------|----------|
| `greeting` | Приветствие в зависимости от времени суток |
| `cards` | Данные по каждой карте (последние 4 цифры, сумма расходов, кешбэк) |
| `top_transactions` | Топ-5 транзакций по сумме платежа |
| `currency_rates` | Курсы валют (USD, EUR) через API |
| `stock_prices` | Цены акций (заглушка, будет доработано) |

### Сервис «Простой поиск»
Функция `search_transactions` в модуле `services.py` позволяет искать транзакции по строке запроса в описании или категории.

### Отчёт «Траты по категории»
Функция `spending_by_category` в модуле `reports.py` рассчитывает сумму трат по заданной категории за последние 3 месяца.

## Технологии

- Python 3.14
- Poetry — управление зависимостями
- pandas — работа с Excel-данными
- requests — запросы к API для курсов валют
- pytest — тестирование (60 passed, 1 skipped)
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

# Запуск тестов
poetry run pytest

# Проверка качества кода
poetry run flake8
poetry run mypy src

# Структура проекта
 
bank_coursework_1/
├── data/
│   └── operations.xlsx      # Excel-файл с транзакциями
├── src/
│   ├── utils.py             # Вспомогательные функции
│   ├── views.py             # Функции для веб-страниц
│   ├── reports.py           # Функции для отчётов (в разработке)
│   └── services.py          # Функции для сервисов (в разработке)
├── tests/                   # Тесты (60 passed, 1 skipped)
├── user_settings.json       # Настройки пользователя (валюты, акции)
├── .env                     # Переменные окружения (API-ключ)
├── pyproject.toml           # Конфигурация Poetry
└── README.md


# Запуск
Запуск тестов
bash

## Запуск всех тестов
pytest

## Запуск с измерением покрытия
pytest --cov=src --cov-report=html

# Проверка стиля кода
bash

## Проверка стиля
flake8

## Форматирование кода
black .

## Сортировка импортов
isort .

## Проверка типов
mypy src

Пример использования
python
from src.views import main_page

# Получить JSON для главной страницы
result = main_page("2021-12-31 15:00:00")
print(result)


## Примеры использования
python

@log()
def my_function(x, y):
    return x + y

@log(filename="mylog.txt")
def another_function():
    # код функции

# Тестирование

Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\__init__.py                0      0   100%
src\decorators.py             32      0   100%
src\external_api.py           61      9    85%   54, 57-60, 73, 75, 78, 110
src\file_readers.py           52     11    79%   27, 52, 58-60, 81-83, 104-106
src\generators.py             13      0   100%
src\masks.py                  39      0   100%
src\operations_parser.py      23      9    61%   24, 29-38
src\processing.py              5      0   100%
src\reports.py                 0      0   100%
src\services.py                0      0   100%
src\utils.py                 134     45    66%   43-64, 77-79, 86-94, 111-115, 142-147, 264-267, 288, 290-291
src\views.py                  14      1    93%   27
src\widget.py                 18      2    89%   44-46
--------------------------------------------------------
TOTAL                        391     77    80%

## Генерация отчета о покрытии
bash

pytest --cov=src --cov-report=html
open htmlcov/index.html

## Вклад в проект

    Создайте новую ветку от develop

    Внесите изменения

    Создайте Pull Request

    Дождитесь ревью
 
 