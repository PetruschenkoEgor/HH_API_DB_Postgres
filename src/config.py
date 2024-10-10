import os
from configparser import ConfigParser

PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "database.ini")


def config(filename: str = PATH_TO_FILE, section: str = "postgresql") -> dict[str, str]:
    # Создание парсера
    parser = ConfigParser()
    # Чтение файла конфигурации
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
