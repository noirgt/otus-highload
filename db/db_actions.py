from db.db_connector import connector
from configuration import REDIS_SERVER
from ast import literal_eval
import redis



@connector(["master"])
def db_setter(first_name, last_name, city_name,
                sex_value, age, hobbie,
                password, token, conn):
    # Создание объекта cursor
    cursor = conn.cursor()
    # Получение идентификатора города по его имени
    cursor.execute("SELECT id FROM cities WHERE name = %s", (city_name,))
    city_id = cursor.fetchone()

    # Если город не найден, добавляем его
    if not city_id:
        cursor.execute("INSERT INTO cities (name) VALUES (%s)", (city_name,))
        conn.commit()
        city_id = cursor.lastrowid
    else:
        city_id = city_id[0]

    # Получение идентификатора пола по его значению
    cursor.execute("SELECT id FROM sex WHERE name = %s", (sex_value,))
    sex_id = cursor.fetchone()

    # Если возраст не найден, добавляем его
    if not sex_id:
        cursor.execute("INSERT INTO sex (name) VALUES (%s)", (sex_value,))
        conn.commit()
        sex_id = cursor.lastrowid
    else:
        sex_id = sex_id[0]

    # Добавление пользователя с использованием идентификаторов города и возраста
    request_values = (
        first_name, last_name, city_id, sex_id, age, hobbie, password, token)
    query = """
        INSERT INTO users
        (first_name, last_name, city_id, sex_id, age, hobbie, password, token)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, request_values)

    # Применение изменений
    conn.commit()

    # Получение идентификатора последней вставленной строки
    last_inserted_id = cursor.lastrowid

    # Закрытие соединения
    cursor.close()

    return last_inserted_id



@connector(["master"])
def db_getter(user_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT users.id as uid, first_name, last_name, cities.name as city,
        sex.name as sex, age, hobbie, password, token
        FROM users
        INNER JOIN cities ON users.city_id = cities.id
        INNER JOIN sex ON users.sex_id = sex.id
        WHERE users.id = %s;
    """
    cursor.execute(query, (user_id,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@connector(["master"])
def db_deleter(user_id, conn):
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    # Применение изменений
    conn.commit()
    # Закрытие соединения
    cursor.close()

    return



@connector(["master"])
def db_token(user_id, user_password, conn):
    cursor = conn.cursor()
    query = "SELECT token FROM users WHERE id = %s AND password = %s;"
    cursor.execute(query, (user_id, user_password))
    result = cursor.fetchone()
    # Закрытие соединения
    cursor.close()

    return result[0]



@connector(["master"])
def db_check_token(user_token, conn):
    cursor = conn.cursor(buffered=True)
    query = "SELECT token FROM users WHERE token = %s;"
    cursor.execute(query, (user_token,))
    result = cursor.fetchone()
    # Закрытие соединения
    cursor.close()

    return result[0]



@connector(["master"])
def db_finder(first_name, last_name, conn):
    # Создание объекта cursor
    cursor = conn.cursor()
    first_name = first_name + "%"
    last_name = last_name + "%"

    query = """
        SELECT users.id as uid, first_name, last_name, cities.name as city,
        sex.name as sex, age, hobbie
        FROM users
        INNER JOIN cities ON users.city_id = cities.id
        INNER JOIN sex ON users.sex_id = sex.id
        WHERE first_name LIKE %s and last_name  LIKE %s;
    """
    cursor.execute(query, (first_name, last_name))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result

@connector(["master"])
def db_get_posts(offset, limit, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT posts.id as post_id, users.first_name,
        users.last_name, content
        FROM posts
        INNER JOIN users ON posts.id = users.id LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (limit, offset))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



def db_get_posts_redis(offset, limit):
    r2_redis = redis.StrictRedis(REDIS_SERVER)
    l = r2_redis.lrange("all_posts", offset, limit)

    posts = []
    for post in l:
        post = post.decode('utf-8')
        post = literal_eval(post)
        posts.append(post)

    return posts
