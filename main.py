import re

from src.user_interaction import (data_preparation, display_menu_company, display_menu_search, get_avg_salary,
                                  get_menu_choice_company, get_menu_choice_search, get_name_company_and_count,
                                  get_vacancy_by_key_word)

COMPANY = "а"
INPUT_COMPANY = "б"
EXIT_C = "в"
NAME = 1
SALARY_AVG = 2
KEY_WORD = 3
EXIT_S = 4


def main():
    """ Главная функция """
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
            choice = EXIT_C

    data_preparation(word_list)

    while choice != EXIT_S:
        display_menu_search()
        choice = get_menu_choice_search()

        if choice == 1:
            get_name_company_and_count()
        elif choice == 2:
            get_avg_salary()
        elif choice == 3:
            words = re.split(", |,", (input("Введите ключевые слова через запятую для поиска вакансий: ")))
            print()
            get_vacancy_by_key_word(words)


if __name__ == '__main__':
    main()
