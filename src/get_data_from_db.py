from typing import Any

import psycopg2


class DBManager:
    """ Подключается к БД PostgreSQL и получает данные из БД """

    db_name: str  # Название БД

    def __init__(self, db_name):
        self.__db_name = db_name

    def get_companies_and_vacancies_count(self, params: dict[str, str]) -> list[dict[str, int]] | None:
        """ Получает список всех компаний и количество вакансий у каждой компании """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name_company, count(name_company) FROM vacancy
                    LEFT JOIN company USING (id_company)
                    GROUP BY name_company
                    """)
                records = cur.fetchall()
                result = []
                for row in records:
                    result_dict = {row[0]: row[1]}
                    result.append(result_dict)

                return result

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self, params: dict[str, str]) -> list[dict[str, set[Any]]] | None:
        """ Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT name_company, name_vacancy, salary_from, salary_to, v.link FROM vacancy v
                    LEFT JOIN company c USING (id_company)
                    """)
                records = cur.fetchall()
                result = []
                for row in records:
                    dict_result = {"name_company": row[0], "name_vacancy": row[1], "salary_from": row[2],
                                   "salary_to": row[3], "link": row[4]}
                    result.append(dict_result)

                return result

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self, params: dict[str, str]) -> int | None:
        """ Получает среднюю зарплату по вакансиям """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            with conn.cursor() as cur:
                cur.execute("SELECT ROUND(AVG(salary_from)) FROM vacancy")
                records_from = cur.fetchone()[0]
                cur.execute("SELECT ROUND(AVG(salary_to)) FROM vacancy")
                records_to = cur.fetchone()[0]

                return round(((records_from + records_to) / 2))

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_higher_salary(self, params: dict[str, str]) -> list[tuple[Any, ...]]:
        """ Получает список всех вакансий, у которых зарплата выше средней максимальной зарплаты по всем вакансиям """
        conn = None
        try:
            avg_salary = self.get_avg_salary(params)
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM vacancy WHERE salary_from > %(avg_salary)s",
                            {"avg_salary": avg_salary})
                records = cur.fetchall()
                result = []
                for row in records:
                    result.append(row)

                return result

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_keyword(self, word_list: list[str], params: dict[str, str]) -> list[tuple[Any, ...]] | None:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            with conn.cursor() as cur:
                result = []
                for word in word_list:
                    cur.execute("""
                        SELECT * FROM vacancy
                        WHERE name_vacancy ILIKE %(word)s
                        """,
                                {'word': '%{}%'.format(word)})
                    records = cur.fetchall()
                    for row in records:
                        result.append(row)

                return result

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()
