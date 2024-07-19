from configuration import \
        db_servers, \
            REDIS_SERVER, REDIS_USER, REDIS_PASSWORD, \
                RMQ_SERVER, RMQ_USER, RMQ_PASSWORD
import mysql.connector
from random import choice
import redis
import pika



def pooller(db_server):
    dbconfig = db_servers[db_server]
    global all_pools
    try:
        if db_server in all_pools:
            return all_pools[db_server]
    except NameError:
        all_pools = {}

    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name=db_server, pool_size=10, **dbconfig)
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



def redis_connector(func):
    def wrapper(*args, **kwargs):
        conn = redis.StrictRedis(host=REDIS_SERVER,
                                 port=6379, db=0,
                                 password=REDIS_PASSWORD,
                                 username=REDIS_USER)
        return func(*args, **kwargs, conn=conn)
    return wrapper



def rmq_connector(ephemeral_conn=True):
    def actual_connector(func):
        def wrapper(*args, **kwargs):
            credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD)
            parameters = pika.ConnectionParameters(RMQ_SERVER,
                                            5672,
                                            '/',
                                            credentials)

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(
                exchange='friend_posts', exchange_type='direct')
            try:
                return func(*args, **kwargs, channel=channel)
            finally:
                if ephemeral_conn:
                    print(ephemeral_conn)
                    print("RMQ CONN CLOSED")
                    connection.close()
        return wrapper
    return actual_connector
