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

    # Структура таблицы posts
    posts_table = """
    CREATE TABLE IF NOT EXISTS posts (
        id INT NOT NULL,
        content TEXT NOT NULL,
        content_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION
    )
    """

    # Структура таблицы followers
    followers_table = """
    CREATE TABLE IF NOT EXISTS followers (
        id INT NOT NULL,
        subscription INT NOT NULL,
        FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION,
        FOREIGN KEY (subscription) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION,
        UNIQUE (id, subscription)
    )
    """

    # Подключение к базе данных
    cursor = conn.cursor()

    # Создание таблиц, если они еще не существуют
    for table in (cities_table, sex_table,
                  users_table, posts_table, followers_table):
        cursor.execute(table)

    # Применение изменений и закрытие соединения
    conn.commit()
    cursor.close()
