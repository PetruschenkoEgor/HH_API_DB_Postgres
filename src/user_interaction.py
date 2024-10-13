import re
from typing import Any

from config.config import config
from src.create_table import PostgresDB
from src.get_data_from_db import DBManager
from src.insert_data_in_table import InsertTablePostgres
from src.utils import join_company_vacancy

COMPANY = "а"
INPUT_COMPANY = "б"
EXIT_C = "в"
NAME_COUNT = 1
VACANCY = 2
SALARY_AVG = 3
HIGH_AVG = 4
KEY_WORD = 5
EXIT_S = 6


def enter_name_of_bd() -> str:
    """ Ввод названия БД """
    print("Привет! Эта программа показывает информацию о компаниях и их вакансиях с сайта HeadHunter! "
          "Вы можете ввести свои компании для поиска или воспользоваться предложенной подборкой компаний!")
    print()
    name_bd = input("Введите название Базы Данных(английскими буквами, без лишних символов, можно с пробелами, "
                    "пример: hh_vacancy): ")
    print()
    # заменяем все символы в строке на '_'
    name_bd = name_bd.translate(str.maketrans({' ': '_', '.': '_', '&': '_', '<': '_', '>': '_', '?': '_', ',': '_'}))
    # проверяем, чтоб первый символ был буквой, если нет, то заменяем его на bd
    if not name_bd[0].isalpha():
        name_bd = name_bd.replace(name_bd[0], "bd")
    print(f"Название вашей Базы Данных: {name_bd}")
    print()

    return name_bd


def enter_count_vacancy() -> int:
    """ Ввод количества вакансий на одну компанию """
    count_vacancy = input("Введите максимальное количество вакансий на одну компанию - число от 1 до 5000(о таком "
                          "количестве вакансий на каждую компанию вы получите информацию): ")
    print()

    while not count_vacancy.isdigit():
        print("Вводить можно числа от 1 до 5000!")
        count_vacancy = input("Введите максимальное количество вакансий на одну компанию(о таком количестве вакансий "
                              "на каждую компанию вы получите информацию): ")
        print()

    count_vacancy = int(count_vacancy)

    if count_vacancy > 5000:
        count_vacancy = 5000
    elif count_vacancy < 1:
        count_vacancy = 1

    return count_vacancy


def display_menu_company() -> None:
    """ Меню главной функции, выбор компаний """
    print("-------Меню выбора компаний-------")
    print("А. Поиск вакансий, 10-ти предложенных компаний")
    print("Б. Ввести свои компании для поиска вакансий")
    print()


def display_menu_search() -> None:
    """ Меню главной функции, что искать в таблицах """
    print("-------Меню поиска-------")
    print("1. Названия всех компаний и количество вакансий у каждой компании")
    print("2. Все вакансии с указанием названия компании, названия вакансии, зарплаты и ссылки")
    print("3. Средняя зарплата по всем вакансиям")
    print("4. Все вакансии, у которых зарплата выше средней зарплаты по всем вакансиям")
    print("5. Вакансии по ключевым словам")
    print("6. Выйти из программы")
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
    choice = input("Введите пункт меню: ")
    print()

    digits = ["1", "2", "3", "4", "5", "6"]
    if choice.isdigit() and choice in digits:
        choice = int(choice)
    else:
        while choice not in digits:
            print("Возможные варианты ввода: 1 - 6")
            choice = input("Введите пункт меню: ")
            print()

        choice = int(choice)

    return choice


def choice_company() -> list[str]:
    """ Выбор: предложенные компании или ввести свои """
    choice = 0
    word_list = []
    while choice != EXIT_C:
        display_menu_company()
        choice = get_menu_choice_company()

        if choice == COMPANY:
            word_list = ["газпром нефть", "ibs", "inlyit", "т-банк", "крафттек", "Кадровое Агентство Averina.agency",
                         "unilever", "DNS Технологии", "тензор", "согаз"]
            choice = EXIT_C
        elif choice == INPUT_COMPANY:
            word_list = re.split(", |,", (input("Введите названия компаний через запятую для поиска: ")))
            print()
            if word_list in [[""], [" "]]:
                print("Вы ввели пустой запрос. Введите компании или выберите готовую подборку")
                print()
            else:
                choice = EXIT_C

    print("Загрузка данных...")
    print()

    return word_list


def choice_action(name_db: str) -> None:
    """ Выбор действия с БД """
    choice = 0
    while choice != EXIT_S:
        display_menu_search()
        choice = get_menu_choice_search()

        if choice == 1:
            get_name_company_and_count(name_db)
        elif choice == 2:
            get_all_vacancy(name_db)
        elif choice == 3:
            get_avg_salary(name_db)
        elif choice == 4:
            get_vacancy_salary_high_avg(name_db)
        elif choice == 5:
            words = re.split(", |,", (input("Введите ключевые слова через запятую для поиска вакансий: ")))
            print()
            get_vacancy_by_key_word(words, name_db)


def data_preparation(words: list[str], name_db: str, count_vacancy: int) -> None | str:
    """ Создание таблиц и заполнение БД """
    # получение компаний и вакансий
    company_vacancy = join_company_vacancy(words, count_vacancy)
    if len(company_vacancy) < 1:
        print("По вашему запросу ничего не нашлось! Попробуйте ввести другие компании или выбрать предложенную "
              "подборку компаний!")
        print()
        # choice_company()
    else:
        # создание БД и таблиц
        data_base = PostgresDB(name_db)
        data_base.create_db(config())
        data_base.create_table(config())

        # заполнение таблиц данными
        insertion = InsertTablePostgres(name_db, company_vacancy)
        insertion.insert_table_company_and_vacancy(config())

        return "ok"


def get_name_company_and_count(name_db: str) -> None:
    """ Получает названия всех компаний и количество вакансий у каждой компании """
    name = DBManager(name_db)
    name = name.get_companies_and_vacancies_count(config())
    for company in name:
        for key, value in company.items():
            print(f"{key}: {value} вакансий")
    print()


def get_all_vacancy(name_db: str) -> None:
    """ Все вакансии с указанием названия компании, названия вакансии, зарплаты и ссылки """
    vacancy = DBManager(name_db)
    vacancy = sorted(vacancy.get_all_vacancies(config()), key=lambda x: x.get("salary_to"))
    vacancy = sorted(vacancy, key=lambda x: x.get("salary_from"))

    for vac in vacancy:
        name_c = vac.get("name_company")
        name_v = vac.get("name_vacancy")
        salary_from = vac.get("salary_from")
        salary_to = vac.get("salary_to")
        link = vac.get("link")
        if salary_from == 0 and salary_to == 0:
            print(f"Название компании: {name_c}. Название вакансии: {name_v}. Зарплата не указана. Ссылка: {link}.")
            print()
        elif salary_from == 0 and salary_to > 0:
            print(f"Название компании: {name_c}. Название вакансии: {name_v}. Зарплата до {salary_to}. "
                  f"Ссылка: {link}.")
            print()
        else:
            print(
                f"Название компании: {name_c}. Название вакансии: {name_v}. Зарплата от {salary_from} до {salary_to}. "
                f"Ссылка: {link}.")
            print()


def get_avg_salary(name_db) -> None:
    """ Средняя зарплата по всем вакансиям """
    avg_salary = DBManager(name_db)
    avg_salary = avg_salary.get_avg_salary(config())
    print(f"Средняя зарплата по вакансиям: {avg_salary} рублей")
    print()


def get_vacancy(vacancy_list: list[tuple[Any, ...]]) -> None:
    """ Перебор вакансий из списка словарей """
    for vacancy in vacancy_list:
        if vacancy[7] == 0 and vacancy[8] == 0:
            print(f"Название вакансии: {vacancy[2]}. Город: {vacancy[3]}. Ссылка: {vacancy[4]}. "
                  f"Зарплата не указана.")
            print()
        elif vacancy[7] == 0 and vacancy[8] > 0:
            print(f"Название вакансии: {vacancy[2]}. Город: {vacancy[3]}. Ссылка: {vacancy[4]}. "
                  f"Зарплата до {vacancy[8]}.")
            print()
        else:
            print(f"Название вакансии: {vacancy[2]}. Город: {vacancy[3]}. Ссылка: {vacancy[4]}. "
                  f"Зарплата от {vacancy[7]} до {vacancy[8]}.")
            print()


def get_vacancy_salary_high_avg(name_db) -> None:
    """ Все вакансии, у которых зарплата выше средней зарплаты по всем вакансиям """
    high_avg = DBManager(name_db)
    high_avg = sorted(high_avg.get_vacancies_with_higher_salary(config()), key=lambda tup: tup[8])
    high_avg = sorted(high_avg, key=lambda tup: tup[7])

    get_vacancy(high_avg)


def get_vacancy_by_key_word(words: list[str], name_db) -> None:
    """ Получение вакансий по ключевым словам """
    if words in [[""], [" "]]:
        print("Вы ввели пустой запрос, переход в меню")
        print()
    else:
        key_word = DBManager(name_db)
        key_word = sorted(key_word.get_vacancies_with_keyword(words, config()), key=lambda tup: tup[8])
        key_word = sorted(key_word, key=lambda tup: tup[7])

        get_vacancy(key_word)
