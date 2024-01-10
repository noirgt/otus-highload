import configuration
import mysql.connector



def connector(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host=configuration.MYSQL_HOST,
            port=configuration.MYSQL_PORT,
            user=configuration.MYSQL_USER,
            password=configuration.MYSQL_PASSWORD,
            database=configuration.MYSQL_DB
        )
        try:
            conn.commit()
            return func(*args, **kwargs, conn=conn)
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()
    return wrapper

