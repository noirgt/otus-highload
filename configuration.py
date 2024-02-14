from os import environ

ADMIN_TOKEN = environ['ADMIN_TOKEN']
REDIS_SERVER = environ['REDIS_SERVER']
db_servers = {
    "master": {
        "host": environ['MYSQL_HOST'],
        "port": environ['MYSQL_PORT'],
        "user": environ['MYSQL_USER'],
        "password": environ['MYSQL_PASSWORD'],
        "database": environ['MYSQL_DATABASE']      
    }
}
