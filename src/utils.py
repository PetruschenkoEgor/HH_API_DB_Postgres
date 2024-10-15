import re

from src.api_company import HeadHunterAPICompany
from src.api_vacancy import HeadHunterAPIVacancy
from src.company import Company
from src.vacancy import Vacancy


def cast_hh_to_object_list_company(companies: list[dict[str | int]]) -> list[Company]:
    """Преобразование набора данных из JSON полученного по API с HH в список экземпляров класса Company"""
    companies_list = []

    for company in companies:
        # Добавление названия, ссылки на компанию, количества открытых вакансий, ссылки на вакансии компании
        company_list = [company.get("name", "Название компании не указано"),
                        company.get("alternate_url", "Ссылка на компанию не указана"),
                        company.get("open_vacancies", "Количество открытых вакансий в компании не указано"),
                        company.get("vacancies_url", "Ссылка на вакансии компании не указана")]

        # Добавление компании(в виде экземпляра класса Company) в список компаний
        companies_list.append((Company(*company_list)))

    return companies_list


def cast_hh_to_object_list_vacancy(vacancies: list[dict[str | int]]) -> list[Vacancy]:
    """Преобразование набора данных из JSON полученного по API с HH в список экземпляров класса Vacancy"""
    vacancies_list = []

    for vacancy in vacancies:
        # Добавление названия вакансии, города, ссылки на вакансию
        vacancy_list = [vacancy.get("name", "Название вакансии не указано"),
                        vacancy.get("area").get("name", "Название города не указано"),
                        vacancy.get("alternate_url", "Ссылка на вакансию не указана")]

        # Добавление краткого описания вакансии
        description = vacancy.get("snippet").get("responsibility")
        if description:
            # Убираем HTML-теги
            description = re.sub(r"<.*?>", "", description)
            vacancy_list.append(description)
        else:
            vacancy_list.append("Описание вакансии отсутствует")

        # Добавление требований к кандидату
        requirements = vacancy.get("snippet").get("requirement")
        if requirements:
            # Убираем HTML-теги
            requirements = re.sub(r"<.*?>", "", requirements)
            vacancy_list.append(requirements)
        else:
            vacancy_list.append("Требования к кандидату отсутствуют")

        # Проверка указана ли зарплата и добавление зарплаты
        salary = vacancy.get("salary")
        if salary:
            salary_from = vacancy.get("salary").get("from")
            salary_to = vacancy.get("salary").get("to")
            if isinstance(salary_from, int) and salary_from > 0:
                vacancy_list.append(salary_from)
                if isinstance(salary_to, int) and salary_to >= salary_from:
                    vacancy_list.append(salary_to)
                else:
                    vacancy_list.append(salary_from)
            else:
                vacancy_list.append(0)
                if isinstance(salary_to, int) and salary_to > 0:
                    vacancy_list.append(salary_to)
        else:
            vacancy_list.append(0)
            vacancy_list.append(0)

        # Добавление вакансии(в виде экземпляра класса Vacancy) в список вакансий
        vacancies_list.append(Vacancy(*vacancy_list))

    return vacancies_list


def join_company_vacancy(companies: list[str], count_vacancy: int) -> list[dict[str, Company | list[Vacancy]]]:
    """ Создает словарь, где ключ - компания, значение - список ее вакансий """
    company_vacancy = []

    for company in companies:
        # Создаем экземпляр класса HeadHunterAPICompany
        com = HeadHunterAPICompany()
        # Получаем json с компанией
        com = com.get_companies(company)
        # Список экземпляров класса Company
        com = cast_hh_to_object_list_company(com)
        # Если вдруг есть компании с одинаковым названием, но записаны в разном регистре
        for comp in com:
            dict_com_vac = {}
            # Ссылка на вакансии компании
            url_vacancies = comp.vacancies_url
            # Создаем экземпляр класса HeadHunterAPIVacancy
            vac = HeadHunterAPIVacancy(url_vacancies, count_vacancy)
            # Получаем json с вакансиями
            vac = vac.get_vacancies()
            # Список экземпляров класса Vacancy
            vac = cast_hh_to_object_list_vacancy(vac)
            dict_com_vac["company"] = comp
            dict_com_vac["vacancy"] = vac
            company_vacancy.append(dict_com_vac)

    return company_vacancy
