from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, send, emit
from mpu9250 import mpu9250

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
imu = mpu9250(mpu_addr=0x69)

@app.route('/')
def hello_world():
    return 'hello'
    #return str(take_sample(10, 'server_sample.csv'))


@app.route('/stef')
def stef():
    return 'Kyle is a betch'


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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000)

