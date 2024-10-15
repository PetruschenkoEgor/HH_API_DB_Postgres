class Company:
    """Класс для создания экземпляра класса Company"""

    name: str  # название компании
    link: str  # ссылка на компанию
    open_vacancies: int  # количество открытых вакансий
    vacancies_url: str  # ссылка на вакансии

    # Список компаний
    companies_list = []

    __slots__ = ("__name", "__link", "__open_vacancies", "__vacancies_url")

    def __init__(self, name, link, open_vacancies, vacancies_url):
        if not name:
            self.__name = "Название компании не указано"
        else:
            self.__name = name
        if not link:
            self.__link = "Ссылка на компанию не указана"
        else:
            self.__link = link
        if not open_vacancies:
            self.__open_vacancies = "Количество открытых вакансий не указано"
        else:
            self.__open_vacancies = open_vacancies
        if not vacancies_url:
            self.__vacancies_url = "Ссылка на вакансии компании не указана"
        else:
            self.__vacancies_url = vacancies_url

    @property
    def name(self) -> str:
        """Геттер для названия компании"""
        return self.__name

    @property
    def link(self) -> str:
        """Геттер для ссылки на компанию"""
        return self.__link

    @property
    def open_vacancies(self) -> int:
        """Геттер для количества открытых вакансий"""
        return self.__open_vacancies

    @property
    def vacancies_url(self) -> str:
        """Геттер для ссылки на вакансии"""
        return self.__vacancies_url
