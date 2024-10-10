from typing import Any

import requests


class HeadHunterAPICompany:
    """Взаимодействие с API, поиск компаний(работодателей)"""

    def __init__(self):
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "only_with_vacancies": True, "page": 0, "per_page": 100}
        self.__companies = []

    def __connect_to_api(self) -> dict[str | list[dict[str | str, int]]] | int | Any:
        """Подключение к API hh.ru"""
        # Гет-запрос
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        # Проверка на успешность запроса
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    @property
    def connect_to_api(self) -> dict[str | list[dict[str | str, int]]] | int | Any:
        """Геттер для метода отправляющего гет-запрос"""
        return self.__connect_to_api()

    def get_companies(self, word: str, per_page: int = 100) -> list[dict[str | int]]:
        """Получение компаний с hh.ru в формате JSON(как есть, не обработанные)"""
        # Если per_page > 100, то это вызовет ошибку. Условие предотвращает эту ошибку
        if per_page > 100:
            per_page = 100

        # В параметрах запроса меняем слово для поиска
        self.__params["text"] = word
        self.__params["per_page"] = per_page
        while self.__params.get("page") != 1:
            # Получение вакансий
            companies = self.connect_to_api["items"]
            company = []
            for com in companies:
                if com.get("name").lower() == word.lower():
                    company.append(com)
            # Добавление вакансий в список
            self.__companies.extend(company)
            # Следующая страница
            self.__params["page"] += 1

        return self.__companies
