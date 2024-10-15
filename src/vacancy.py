class Vacancy:
    """Класс для создания экземпляров класса Vacancy"""

    name: str  # название вакансии
    area: str  # город
    link: str  # ссылка на вакансию
    description: str  # краткое описание вакансии
    requirements: str  # требования к кандидату
    salary_from: int  # зарплата от
    salary_to: int  # зарплата до

    # Список вакансий
    vacancies_list = []

    __slots__ = ("__name", "__area", "__link", "__description", "__requirements", "__salary_from", "__salary_to")

    def __init__(self, name, area, link, description, requirements, salary_from, salary_to):
        if not name:
            self.__name = "Название вакансии не указано"
        else:
            self.__name = name
        if not area:
            self.__area = "Город не указан"
        else:
            self.__area = area
        if not link:
            self.__link = "Ссылка на вакансию не указана"
        else:
            self.__link = link
        if not description:
            self.__description = "Краткое описание вакансии не указано"
        else:
            self.__description = description
        if not requirements:
            self.__requirements = "Требования к кандидату не указаны"
        else:
            self.__requirements = requirements
        if isinstance(salary_from, int) and salary_from > 0:
            self.__salary_from = salary_from
        else:
            self.__salary_from = 0
        if isinstance(salary_to, int) and salary_to >= salary_from:
            self.__salary_to = salary_to
        else:
            self.__salary_to = salary_from

    @property
    def name(self) -> str:
        """Геттер для названия вакансии"""
        return self.__name

    @property
    def area(self) -> str:
        """Геттер для города"""
        return self.__area

    @property
    def link(self) -> str:
        """Геттер для ссылки на вакансию"""
        return self.__link

    @property
    def salary_from(self) -> int:
        """Геттер для зарплаты от"""
        return self.__salary_from

    @property
    def salary_to(self) -> int:
        """Геттер для зарплаты до"""
        return self.__salary_to

    @property
    def description(self) -> str:
        """Геттер для краткого описания"""
        return self.__description

    @property
    def requirements(self) -> str:
        """Геттер для требований к кандидату"""
        return self.__requirements
