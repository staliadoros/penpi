from flask import Flask
from flask import render_template
from imu_sample import take_sample
app = Flask(__name__)

@app.route('/')
def hello_world():
    return str(take_sample(10, 'server_sample.csv'))

@app.route('/stef')
def stef():
    return 'Kyle is a betch'

@app.route('/view')
@app.route('/view/<user_name>')
def sammy(user_name='default'):
    return render_template('site/index.html', name=user_name)

app.run(host='0.0.0.0',port=5000)
