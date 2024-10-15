from src.user_interaction import choice_action, choice_company, data_preparation, enter_count_vacancy, enter_name_of_bd


def main():
    """ Главная функция """
    data = None

    name_db = enter_name_of_bd()
    count_vacancy = enter_count_vacancy()

    while data != "ok":
        word_list = choice_company()
        data = data_preparation(word_list, name_db, count_vacancy)

    print("Данные успешно загрузились! Выберите какое действие необходимо выполнить!")
    print()

    choice_action(name_db)


if __name__ == '__main__':
    main()
