# 2022-1-QAPYTHON-VK-E-GOLUBETS
Здесь собрано портфолио в рамках курса от VK по автотестированию на Python

## 1. Homework1 - Selenium UI
Что было сделано:
* Тест на логин
* Тест на логаут
* Тест на редактирование контактной информации в профиле https://target.my.com/profile/contacts
* Параметризованный тест на переход на страницы портала через кнопки меню

## 2. Homework2 - Selenium UI. Page Object, Allure, Selenoid
Что было сделано:
* 2 негативных теста на авторизацию
* Тест на создание сегмента
* Тест на удаление сегмента
* Тест на создание кампании
* Весь код реализован c использованием паттерна Page Object
* Возможность просмотреть отчеты в Allure
* Возможность запустить UI тесты в контейнере

## 3. Homework3 - API 
Что было сделано:
API клиент с возможностью авторизации на портале
* Тест на создание кампании и ее автоматическое удаление после теста
* Тест на создание сегмента с проверкой того, что сегмент был создан
* Тест на удаление сегмента

## 5. Homework5 - Log Analyzer Bash and Python (Pandas)
Что было сделано:
* Написаны скрипты на Bash для анализа логов nginx сервера
* Написаны скрипты на Python для анализа логов nginx сервера
* Настроен флаг --json для Python
### Инструкция
Необходимо поместить файл с логами сервера в директорию bash/Python

## 6. Homework6 - ORM
Что было сделано:
* Переписан скрипт из Log Analyzer под использование в pytest
* Создана mysql БД для результатов подсчета из тестов, БД пересоздается при каждом запуске тестов
* Каждое задание заливается в отдельную таблицу
* Задание реализовано в соответствии с концепцией ORM (sqlalchemy)

## 7. Homework7 - Mock 
* Реализован собственный HTTP клиент с помощью библиотеки socket
* Реализован Mock сервер с обработкой PUT и DELETE
* Написал тесты для проверки корректности Mock сервера
