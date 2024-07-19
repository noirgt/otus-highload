from os import environ

ADMIN_TOKEN = environ['ADMIN_TOKEN']
REDIS_SERVER = environ['REDIS_SERVER']
REDIS_USER = environ['REDIS_USER']
REDIS_PASSWORD = environ['REDIS_PASSWORD']
RMQ_SERVER = environ['RABBITMQ_SERVER']
RMQ_USER = environ['RABBITMQ_DEFAULT_USER']
RMQ_PASSWORD = environ['RABBITMQ_DEFAULT_PASS']
db_servers = {
    "master": {
        "host": environ['MYSQL_HOST'],
        "port": environ['MYSQL_PORT'],
        "user": environ['MYSQL_USER'],
        "password": environ['MYSQL_PASSWORD'],
        "database": environ['MYSQL_DATABASE']      
    }
}
