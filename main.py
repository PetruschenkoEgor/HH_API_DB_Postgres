import re

from src.user_interaction import (data_preparation, display_menu_company, display_menu_search, get_all_vacancy,
                                  get_avg_salary, get_menu_choice_company, get_menu_choice_search,
                                  get_name_company_and_count, get_vacancy_by_key_word, get_vacancy_salary_high_avg)

COMPANY = "а"
INPUT_COMPANY = "б"
EXIT_C = "в"
NAME_COUNT = 1
VACANCY = 2
SALARY_AVG = 3
HIGH_AVG = 4
KEY_WORD = 5
EXIT_S = 6


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
            if word_list in [[""], [" "]]:
                print("Вы ввели пустой запрос. Введите компании или выберите готовую подборку")
                print()
            else:
                choice = EXIT_C

    print("Загрузка данных...")
    print()

    data_preparation(word_list)

    while choice != EXIT_S:
        display_menu_search()
        choice = get_menu_choice_search()

        if choice == 1:
            get_name_company_and_count()
        elif choice == 2:
            get_all_vacancy()
        elif choice == 3:
            get_avg_salary()
        elif choice == 4:
            get_vacancy_salary_high_avg()
        elif choice == 5:
            words = re.split(", |,", (input("Введите ключевые слова через запятую для поиска вакансий: ")))
            print()
            get_vacancy_by_key_word(words)


if __name__ == '__main__':
    main()
