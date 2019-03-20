from flask import Flask
from imu_sample import take_sample
app = Flask(__name__)

@app.route('/')
def hello_world():
    return str(take_sample(10, 'server_sample.csv'))

@app.route('/stef')
def stef():
    return 'Kyle is a betch'

app.run(host='0.0.0.0',port=5000)
