## Локальный запуск приложения
- Создать в корне проекта файл `.env` с переменными для доступа к БД и с токеном администратора для авторизации в API:
    ```bash
    MYSQL_ROOT_PASSWORD=root_password
    MYSQL_DATABASE=database
    MYSQL_USER=user
    MYSQL_PASSWORD=user_password
    ADMIN_TOKEN=mytoken
    REDIS_SERVER=redis
    REDIS_SERVER=redis
    REDIS_USER=default
    REDIS_PASSWORD=default_password
    RABBITMQ_SERVER=rabbitmq
    RABBITMQ_DEFAULT_USER=rmq_username
    RABBITMQ_DEFAULT_PASS=rmq_password

    ```
- Запустить docker compose, который активирует сборку и старт контейнера с API и экземпляр БД MySQL:
    ```bash
    docker-compose up -d
    ```
- Сервер будет доступен - `0.0.0.0:8000`
- Авторизацию производить по токену `ADMIN_TOKEN`, либо по токену пользователя после его создания
- Информация по методам API находится в файле `OTUS.postman_collection.json`