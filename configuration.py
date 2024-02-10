from os import environ

ADMIN_TOKEN = environ['ADMIN_TOKEN']
db_servers = {
    "master": {
        "host": environ['MYSQL_HOST'],
        "port": environ['MYSQL_PORT'],
        "user": environ['MYSQL_USER'],
        "password": environ['MYSQL_PASSWORD'],
        "database": environ['MYSQL_DATABASE']      
    },
    "slave": {
        "host": environ['MYSQL_SLAVE_HOST'],
        "port": environ['MYSQL_PORT'],
        "user": environ['MYSQL_USER'],
        "password": environ['MYSQL_PASSWORD'],
        "database": environ['MYSQL_DATABASE']      
    },
    "slave_second": {
        "host": environ['MYSQL_SLAVE_SECOND_HOST'],
        "port": environ['MYSQL_PORT'],
        "user": environ['MYSQL_USER'],
        "password": environ['MYSQL_PASSWORD'],
        "database": environ['MYSQL_DATABASE']      
    }
}
