from db.db_connector import connector



@connector(["master"])
def db_create(conn):
    # Структура таблицы cities
    cities_table = """
    CREATE TABLE IF NOT EXISTS cities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(64) NOT NULL
    )
    """

    # Структура таблицы sex
    sex_table = """
    CREATE TABLE IF NOT EXISTS sex (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(64) NOT NULL
    )
    """

    # Структура таблицы users
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(64) NOT NULL,
        last_name VARCHAR(64) NOT NULL,
        city_id INT,
        sex_id INT,
        age INT,
        hobbie VARCHAR(255),
        password VARCHAR(255) NOT NULL,
        token VARCHAR(255) NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE ON UPDATE NO ACTION,
        FOREIGN KEY (sex_id) REFERENCES sex(id) ON DELETE CASCADE ON UPDATE NO ACTION
    )
    """

    # Подключение к базе данных
    cursor = conn.cursor()

    # Создание таблиц, если они еще не существуют
    cursor.execute(cities_table)
    cursor.execute(sex_table)
    cursor.execute(users_table)

    # Применение изменений и закрытие соединения
    conn.commit()
    cursor.close()
