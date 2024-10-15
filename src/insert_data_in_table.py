import psycopg2


class InsertTablePostgres:
    """ Заполняет данными таблицы """

    db_name: str  # Название БД
    data: list  # Список словарей с данными о компаниях и вакансиях

    def __init__(self, db_name, data):
        self.__db_name = db_name
        self.__data = data

    def insert_table_company_and_vacancy(self, params: dict[str, str]) -> None:
        """ Заполняет данными таблицы company и vacancy """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **params)
            for company in self.__data:
                com = company.get("company")
                vacancy = company.get("vacancy")
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO company (name_company, link, open_vacancies, vacancies_url)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id_company
                        """,
                                (com.name, com.link, com.open_vacancies, com.vacancies_url)
                                )
                    id_company = cur.fetchone()[0]
                    for vac in vacancy:
                        cur.execute("""
                            INSERT INTO vacancy
                            (id_company, name_vacancy, area, link, description, requirements, salary_from, salary_to)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                                    (id_company, vac.name, vac.area, vac.link, vac.description, vac.requirements,
                                     vac.salary_from, vac.salary_to)
                                    )

            conn.commit()

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()
