# Банковский виджет операций
## Описание проекта

Проект представляет собой набор инструментов для обработки банковских операций. Основные функции включают фильтрацию и сортировку операций по различным критериям.

## Установка

Требования

    Python 3.14+

    Poetry для управления зависимостями

### Установка проекта
bash

# Клонирование репозитория
git clone https://github.com/Alexander-Sky/bankoperation_13_2.git
cd bankoperation_13_2

## Установка зависимостей через Poetry

poetry install
poetry shell

# Установка инструментов разработки
poetry add --group lint flake8 black isort mypy pytest
poetry add --group dev pytest-cov

# Структура проекта
Основные модули

    masks.py - функции маскирования номеров карт и счетов

    widget.py - функции форматирования данных для отображения

    processing.py - функции обработки операций

    generators.py - функции генерации тестовых данных

    conftest.py - фикстуры для тестирования

    external_api.py - работа с внешними API (курсы валют)

    operations_parser.py - парсер операций из JSON

    utils.py - вспомогательные функции
    
    file_readers.py - чтение финансовых операций из CSV и Excel файлов

## Работа с файлами
python

from src.file_readers import read_csv_file, read_excel_file

# Чтение CSV файла
csv_transactions = read_csv_file('data/transactions.csv')

# Чтение Excel файла
excel_transactions = read_excel_file('data/transactions_excel.xlsx')

Инструменты разработки

    isort - сортировка импортов

    black - форматирование кода

    flake8 - проверка стиля кода

    mypy - статическая типизация

    pytest - тестирование

    coverage - измерение покрытия

# Запуск
Запуск тестов
bash

## Запуск всех тестов
pytest

## Запуск с измерением покрытия
pytest --cov=src --cov-report=html

Проверка стиля кода
bash

## Проверка стиля
flake8

## Форматирование кода
black .

## Сортировка импортов
isort .

## Проверка типов
mypy src

Использование
Импорт функций
python

from src.processing import filter_by_state, sort_by_date
from generators.generators import card_number_generator

## Примеры работы
Фильтрация операций
python

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

### Фильтрация по умолчанию (EXECUTED)
filtered_operations = filter_by_state(operations)

### Фильтрация по CANCELED
cancelled_operations = filter_by_state(operations, 'CANCELED')

Декоратор логирования
Описание

Декоратор log предназначен для логирования выполнения функций.
Параметры

    filename (опционально) - имя файла для записи логов

## Примеры использования
python

@log()
def my_function(x, y):
    return x + y

@log(filename="mylog.txt")
def another_function():
    # код функции

# Тестирование

    Текущее покрытие: 84%
    Покрытие нового модуля file_readers.py: 79%
    Цель: 100% покрытие тестами

## Генерация отчета о покрытии
bash

pytest --cov=src --cov-report=html
open htmlcov/index.html

## Вклад в проект

    Создайте новую ветку от develop

    Внесите изменения

    Создайте Pull Request

    Дождитесь ревью
 
 