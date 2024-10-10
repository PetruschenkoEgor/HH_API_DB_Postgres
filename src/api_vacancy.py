from typing import Any

import requests


class HeadHunterAPIVacancy:
    """Взаимодействие с API, получение вакансий"""

    url: str  # ссылка на вакансии

    def __init__(self, url):
        """Конструктор для класса HeadHunterAPI"""
        self.__url = url
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

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

    def get_vacancies(self) -> list[dict[str | int]]:
        """Получение вакансий с hh.ru в формате JSON(как есть, не обработанные)"""
        while self.__params.get("page") != 1:
            # Получение вакансий
            vacancies = self.connect_to_api["items"]
            # Добавление вакансий в список
            self.__vacancies.extend(vacancies)
            # Следующая страница
            self.__params["page"] += 1

        return self.__vacancies
