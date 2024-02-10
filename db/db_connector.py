from configuration import db_servers
import mysql.connector
from random import choice



def pooller(db_server):
    dbconfig = db_servers[db_server]
    global all_pools
    try:
        if db_server in all_pools:
            return all_pools[db_server]
    except NameError:
        all_pools = {}

    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name=db_server, pool_size=1, **dbconfig)
    all_pools[db_server] = pool
    return pool



def connector(conn_db_servers):
    def actual_connector(func):
        def wrapper(*args, **kwargs):
            db_server = choice(conn_db_servers)
            pool = pooller(db_server)
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
    return actual_connector
