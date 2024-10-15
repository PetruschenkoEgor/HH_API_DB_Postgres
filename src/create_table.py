import psycopg2


class PostgresDB:
    """ Создание БД и таблиц """

    def __init__(self, db_name):
        self.__db_name = db_name

    def create_db(self, param: dict[str, str]) -> None:
        """ Создание БД """
        conn = None
        try:
            # подключение к БД
            conn = psycopg2.connect(dbname='postgres', **param)
            # автоматическое сохранение изменений
            conn.autocommit = True
            # создание курсора
            with conn.cursor() as cur:
                # если БД уже существует, то удалим ее, чтобы не было ошибок
                cur.execute(f"DROP DATABASE IF EXISTS {self.__db_name}")
                # создание БД
                cur.execute(f"CREATE DATABASE {self.__db_name}")

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()

    def create_table(self, param: dict[str, str]) -> None:
        """ Создание таблиц company и vacancy """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.__db_name, **param)
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE company (
                        id_company SERIAL PRIMARY KEY,
                        name_company VARCHAR NOT NULL,
                        link VARCHAR,
                        open_vacancies INTEGER,
                        vacancies_url VARCHAR
                    )
                """)

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE vacancy (
                        id_vacancy SERIAL PRIMARY KEY,
                        id_company INTEGER REFERENCES company(id_company),
                        name_vacancy VARCHAR NOT NULL,
                        area VARCHAR,
                        link VARCHAR,
                        description TEXT,
                        requirements TEXT,
                        salary_from INTEGER,
                        salary_to INTEGER
                    )
                """)

            conn.commit()

        except psycopg2.Error as error:
            print(f"Ошибка БД:{error}")

        except Exception as error:
            print(f"Ошибка: {error}")

        finally:
            if conn is not None:
                conn.close()
