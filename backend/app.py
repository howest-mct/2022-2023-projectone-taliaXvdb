#BACKEND IMPORT
import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

#GPIO IMPORT
from RPi import GPIO
import time
import board
from helpers.gewichtssensor import HX711
from helpers.temperatuursensor import DS18B20
from helpers.trilmotor import VibrationMotor
from helpers.ledring import leds
from helpers.buzzer import reminder
from helpers.LCD import LCDpcfClass

#REGION GPIO, PIN DEFINING
btn = 21
lcdPins = {
    'rs': 26,
    'e': 19
}

weightPins = {
    'dt': 25,
    'sck': 18
}

hx711 = HX711(weightPins['dt'], weightPins['sck'])
ds18b20 = DS18B20()
buzz = reminder(16)
lcd = LCDpcfClass(lcdPins['rs'], lcdPins['e'])
brrr = VibrationMotor(23)
ledring = leds(24, board.D12, 0.1)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn, GPIO.IN)
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=callback_button, bouncetime=300)
    lcd.set_cursor()
    hx711.setup()

def loop():
    pass

def callback_button(pin):
    print('button pressed')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

# API ENDPOINTS

# regio ROUTES
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

ENDPOINT = 'api/v1/waterreminder'

@app.route(ENDPOINT + '/users/', methods= ['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = DataRepository.read_all_users()
        return jsonify(data=result), 200
    elif request.method == 'POST':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.create_user(form['name'], form['goal'], form['streak'])
        if data is not None:
            return jsonify(status='OK', data=data), 201
        else:
            return jsonify(status='ERROR'), 500
        
@app.route(ENDPOINT + '/user/<id>/', methods=['GET', 'PUT', 'DELETE'])
def user(id):
    if request.method == 'GET':
        user = DataRepository.read_user(id)
        history = DataRepository.read_history_by_userid(id)
        return jsonify(user=user, history = history), 200
    elif request.method == 'PUT':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.update_user(id, form['name'], form['goal'], form['streak'])
        if data is not None:
            if data > 0:
                return jsonify(status='OK', data=id), 201
            else:
                return jsonify(status='NO CHANGES'), 200
        else:
            return jsonify(status='ERROR'), 500
    elif request.method == 'DELETE':
        return jsonify(status='DELETED', id=DataRepository.delete_user(id))
    
@app.route(ENDPOINT + '/history/', methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        result = DataRepository.read_history()
        return jsonify(data=result), 200
    elif request.method == 'POST':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.create_reading(form['deviceID'], form['actionID'], form['userID'], form['date'], form['value'], form['comment'])
        if data is not None:
            return jsonify(status='OK', data=data), 201
        else:
            return jsonify(status='ERROR'), 500
    
@app.route(ENDPOINT + '/reminders/', methods=['GET'])
def all_reminders():
    if request.method == 'GET':
        result = DataRepository.read_all_reminders()
        return jsonify(data=result), 200
    
@app.route(ENDPOINT + '/user/<iduser>/reminders/', methods= ['GET', 'POST'])
def reminders(iduser):
    if request.method == 'GET':
        user = DataRepository.read_user(iduser)
        reminders = DataRepository.read_reminders_by_userid(iduser)
        return jsonify(user=user, reminders = reminders), 200
    elif request.method == 'POST':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.create_reminder(iduser, form['type'], form['time'], form['amount'], form['fasterWhenHot'])
        if data is not None:
            return jsonify(status='OK', data=data), 201
        else:
            return jsonify(status='ERROR'), 500
        
@app.route(ENDPOINT + '/user/<iduser>/reminders/<reminderid>/', methods=['GET', 'PUT', 'DELETE'])
def reminder(iduser, reminderid):
    if request.method == 'GET':
        reminder = DataRepository.read_one_reminder(reminderid)
        return jsonify(reminder = reminder), 200
    elif request.method == 'PUT':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.update_reminder(reminderid, iduser, form['type'], form['time'], form['amount'], form['fasterWhenHot'])
        if data is not None:
            if data > 0:
                return jsonify(status='OK', data=id), 201
            else:
                return jsonify(status='NO CHANGES'), 200
        else:
            return jsonify(status='ERROR'), 500
    elif request.method == 'DELETE':
        return jsonify(status='DELETED', id=DataRepository.delete_reminder(reminderid))


# regio SOCKETIO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!



if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print("finished")
