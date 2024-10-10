from src.config import config
from src.create_table import PostgresDB
from src.get_data_from_db import DBManager
from src.insert_data_in_table import InsertTablePostgres
from src.utils import join_company_vacancy


def display_menu_company() -> None:
    """ Меню главной функции, выбор компаний """
    print("Привет! Эта программа показывает информацию о 10 компаниях с сайта HeadHunter, которые я подобрал! "
          "Или ты можешь вписать свои компании!")
    print("Так как это учебный проект, для удобства глубина поиска ограничена 100 "
          "вакансиями для каждой компании. ")
    print()
    print("-------Меню выбора компаний-------")
    print("А. Поиск вакансий, 10-ти предложенных компаний")
    print("Б. Ввести свои компании для поиска вакансий")
    print()


def display_menu_search() -> None:
    """ Меню главной функции, что искать в таблицах """
    print("-------Меню поиска-------")
    print("1. Названия всех компаний и количество вакансий у каждой компании")
    print("2. Средняя зарплата по всем вакансиям")
    print("3. Вакансии по ключевым словам")
    print("4. Выйти из программы")
    print()


def get_menu_choice_company() -> str:
    """ Получает от пользователя пункт меню """
    choice = input("Введите пункт меню: ").lower()
    print()

    # проверка вводимых данных
    while choice not in ["а", "б"]:
        print("Возможные варианты ввода: А, Б(в нижнем или верхнем регистре)")
        choice = input("Введите пункт меню: ").lower()
        print()

    return choice


def get_menu_choice_search() -> int:
    """ Получает от пользователя пункт меню """
    choice = int(input("Введите пункт меню: "))
    print()

    # проверка вводимых данных
    while choice < 1 or choice > 4:
        print("Возможные варианты ввода: 1 - 4")
        choice = int(input("Введите пункт меню: "))
        print()

    return choice


def data_preparation(words: list[str]) -> None:
    """ Создание таблиц и заполнение БД """
    # получение компаний и вакансий
    company_vacancy = join_company_vacancy(words)

    # создание БД и таблиц
    data_base = PostgresDB('hhapi')
    data_base.create_db(config())
    data_base.create_table(config())

    # заполнение таблиц данными
    insertion = InsertTablePostgres('hhapi', company_vacancy)
    insertion.insert_table_company_and_vacancy(config())


def get_name_company_and_count() -> None:
    """ Получает названия всех компаний и количество вакансий у каждой компании """
    name = DBManager('hhapi')
    name = name.get_companies_and_vacancies_count(config())
    for company in name:
        for key, value in company.items():
            print(f"{key}: {value} вакансий")
    print()


def get_avg_salary() -> None:
    """ Средняя зарплата по всем вакансиям """
    avg_salary = DBManager('hhapi')
    avg_salary = avg_salary.get_avg_salary(config())
    print(f"Средняя зарплата по вакансиям: {avg_salary} рублей")
    print()


def get_vacancy_by_key_word(words: list[str]) -> None:
    """ Получение вакансий по ключевым словам """
    key_word = DBManager('hhapi')
    key_word = sorted(key_word.get_vacancies_with_keyword(words, config()), key=lambda tup: tup[7])
    for vacancy in key_word:
        if vacancy[7] == 0 and vacancy[8] == 0:
            print(f"Название вакансии: {vacancy[2]}. Город: {vacancy[3]}. Ссылка: {vacancy[4]}. "
                  f"Зарплата не указана.")
            print()
        else:
            print(f"Название вакансии: {vacancy[2]}. Город: {vacancy[3]}. Ссылка: {vacancy[4]}. "
                  f"Зарплата от {vacancy[7]} до {vacancy[8]}.")
            print()
