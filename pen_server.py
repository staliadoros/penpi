from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, send, emit
from mpu9250 import mpu9250
import threading



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
imu = mpu9250(mpu_addr=0x69)

# global variables
sample_rate = 1.0/80.0  # seconds
signal_buffer = []


# background timer function
def add_to_buffer():
    signal_buffer.append(imu.accel)

# background timer object
signal_timer = threading.Timer(sample_rate, add_to_buffer)

@app.route('/')
def hello_world():
    return 'hello'


@app.route('/view')
@app.route('/view/<user_name>')
def view(user_name='default'):
    return render_template('index.html', name=user_name)


@socketio.on('initial_connect')
def handle_initial_connection(message):
    print('received message: ' + message['data'])
    send_data()


@socketio.on('request_data')
def send_data():
    axes = ['x', 'y', 'z']
    accel_data = list(imu.accel)
    accel_dict = dict(zip(axes, accel_data))
    emit('new_data', accel_dict)


#@socketio.on('begin_collection')
@app.route('/start_collect')
def start_data_collection():

    # pull signal buffer from global scope
    global signal_buffer

    # clear buffer
    signal_buffer = []

    # start timer
    signal_timer.start()

    return 'Started fresh data collection!'


#@socketio.on('end_collection')
@app.route('/stop_collect')
def stop_data_collection():

    # pull signal buffer from global scope
    global signal_buffer

    # stop the timer
    signal_timer.stop()

    return signal_buffer


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000)
