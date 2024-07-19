from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from app import auth
from users import Users
from db.db_connector import rmq_connector, redis_connector
import sys
import json


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')
user = Users()



@redis_connector
def db_set_posts_redis(data, conn):
    routing_key = session['uid']
    key_name = f"socket-{routing_key}"
    data = json.dumps(data)
    conn.set(name=key_name, value=data)



@redis_connector
def db_get_posts_redis(conn):
    routing_key = session['uid']
    key_name = f"socket-{routing_key}"
    data = conn.get(key_name)

    if not data:
        return {}
    return json.loads(data)



@rmq_connector(ephemeral_conn=False)
def connection_rmq(channel):
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    return (channel, queue_name)



def receive_rmq(channel, queue):
    channel.queue_bind(
        exchange='friend_posts', queue=queue, routing_key=session['uid'])

    # Получаем сообщение из очереди (до тех пор, пока очередь не пуста)
    method_frame, header_frame, body = channel.basic_get(
        queue=queue, auto_ack=True)

    data = db_get_posts_redis()

    if method_frame:
        message = body.decode('utf-8')
        message = json.loads(message)
        f_name = message['first_name']
        l_name = message['last_name']
        content = message['content']
        post_id = message['post_id']

        # session.setdefault('data', {}).update({
        #     f'{post_id}: {l_name} {f_name}': content
        # })
        data[f'{post_id}: {l_name} {f_name}'] = content
        db_set_posts_redis(data)



@app.route('/post/feed/posted')
@auth.login_required
def main():
    return render_template(
        'index.html', table_data={})




@socketio.on("my_event")
def update_table_data():
    user.user_my_token = request.headers.get('Authorization').split()[1]
    session['uid'] = str(user.user_my_uid)
    rmq_conn = session.get('rmq', {})

    if not rmq_conn:
        rmq_conn = connection_rmq()
        session['rmq'] = (rmq_conn[0], rmq_conn[1])

    receive_rmq(session['rmq'][0], session['rmq'][1])

    #data = session.get('data', {})
    data = db_get_posts_redis()
    socketio.emit('update_table', data, room=request.sid)
    socketio.sleep(1)

if __name__ == '__main__':
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=1240)
    except:
        sys.exit(1)
