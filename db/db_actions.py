from db.db_connector import connector, redis_connector, rmq_connector
import json



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
def db_set_posts(user_my_id, content, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        INSERT INTO posts (id, content)
        VALUES
        (%s, %s);
    """
    cursor.execute(query, (user_my_id, content))
    conn.commit()

    query = """
        SELECT content_id FROM posts
        WHERE id = %s AND content = %s
        ORDER BY content_id DESC LIMIT 1;
    """
    cursor.execute(query, (user_my_id, content))

    # Получение результатов
    result = cursor.fetchone()

    # Закрытие соединения
    cursor.close()

    return result[0]



@connector(["master"])
def db_del_posts(user_my_id, content_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        DELETE FROM posts 
        WHERE id = %s AND content_id = %s;
    """
    cursor.execute(query, (user_my_id, content_id))

    # Закрытие соединения
    conn.commit()
    cursor.close()



@connector(["master"])
def db_get_posts(content_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT posts.content_id as post_id, users.first_name,
        users.last_name, content
        FROM posts
        INNER JOIN users ON posts.id = users.id
        WHERE content_id = %s;
    """
    cursor.execute(query, (content_id,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@connector(["master"])
def db_get_all_posts(offset, limit, user_my_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT posts.content_id as post_id, users.first_name,
        users.last_name, content
        FROM posts
        INNER JOIN users ON posts.id = users.id
        WHERE users.id IN (SELECT subscription FROM followers WHERE id = %s)
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (user_my_id, limit, offset,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@connector(["master"])
def db_get_my_user_id(token, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT id FROM users WHERE token = %s;
    """
    cursor.execute(query, (token,))

    # Получение результатов
    result = cursor.fetchone()

    # Закрытие соединения
    cursor.close()

    return result[0]



@connector(["master"])
def db_set_followers(user_my_id, subscription_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        INSERT INTO followers (id, subscription)
        VALUES
        (%s, %s);
    """
    cursor.execute(query, (user_my_id, subscription_id))

    # Закрытие соединения
    conn.commit()
    cursor.close()



@connector(["master"])
def db_del_followers(user_my_id, subscription_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        DELETE FROM followers
        WHERE id = %s AND subscription = %s;
    """
    cursor.execute(query, (user_my_id, subscription_id))

    # Закрытие соединения
    conn.commit()
    cursor.close()



@connector(["master"])
def db_get_followers(user_my_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT users.id, users.first_name, users.last_name
        FROM followers
        INNER JOIN users ON followers.subscription = users.id
        WHERE followers.id = %s;
    """
    cursor.execute(query, (user_my_id,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@connector(["master"])
def db_get_my_followers_ids(user_my_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT id FROM followers WHERE subscription = %s;
    """
    cursor.execute(query, (user_my_id,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@connector(["master"])
def db_set_dialogs(user_id, text, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        INSERT INTO dialogs (user_id, dialog)
        VALUES
        (%s, %s);
    """
    cursor.execute(query, (user_id, text))

    # Закрытие соединения
    conn.commit()
    cursor.close()



@connector(["master"])
def db_get_dialogs(user_id, conn):
    # Создание объекта cursor
    cursor = conn.cursor()

    query = """
        SELECT * FROM dialogs WHERE user_id = %s;
    """
    cursor.execute(query, (user_id,))

    # Получение результатов
    result = cursor.fetchall()

    # Закрытие соединения
    cursor.close()

    return result



@redis_connector
def db_set_posts_redis(offset, limit, user_my_id, conn, ttl=60):
    key_name  = str(hash((offset, limit, user_my_id)))
    data = db_get_all_posts(offset, limit, user_my_id)
    data = json.dumps(data)
    conn.setex(key_name, ttl, data)
    return data


@redis_connector
def db_get_posts_redis(offset, limit, user_my_id, conn):
    key_name = str(hash((offset, limit, user_my_id)))

    data = conn.get(key_name)
    if not data:
        data = db_set_posts_redis(offset, limit, user_my_id)
    return json.loads(data)


@rmq_connector()
def db_set_posts_rmq(user_my_id, content, post_id, channel):
    my_user_info = db_getter(user_my_id)[0]
    my_user_first_name = my_user_info[1]
    my_user_last_name =  my_user_info[2]
    my_followers_ids = db_get_my_followers_ids(user_my_id)

    for follower_id in my_followers_ids:
        message = {
            "first_name": my_user_first_name,
            "last_name": my_user_last_name,
            "content": content,
            "post_id": post_id
        }
        message = json.dumps(message)
        routing_key = str(follower_id[0])

        channel.basic_publish(
            exchange='friend_posts', routing_key=routing_key, body=message)

        print(f"RMQ [x] Sent {message}")
