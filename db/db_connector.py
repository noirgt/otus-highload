import configuration
import mysql.connector



def pooller():
    dbconfig = {
        "host": configuration.MYSQL_HOST,
        "port": configuration.MYSQL_PORT,
        "user": configuration.MYSQL_USER,
        "password": configuration.MYSQL_PASSWORD,
        "database": configuration.MYSQL_DB
    }
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="otus_app_pool", pool_size=1, **dbconfig)
    return pool



def connector(func):
    def wrapper(*args, **kwargs):
        global pool
        try:
            conn = pool.get_connection()
        except NameError:
            pool = pooller()
            conn = pool.get_connection()
        try:
            conn.commit()
            return func(*args, **kwargs, conn=conn)
        except Exception as e:
             print(f"An error occurred: {e}")
             conn.rollback()
        finally:
            conn.close()
    return wrapper
