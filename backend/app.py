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
from helpers.rfid import RFid

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
rfid = RFid()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn, GPIO.IN)
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=callback_button, bouncetime=300)
    lcd.set_cursor()
    lcd.clear_lcd()
    hx711.setup()

def loop():
    temp = ds18b20.read_temp()
    weight = hx711.get_weight()
    # create_measurement(1,1, 2, time.gmtime(), temp, 'Temperature measured')
    # create_measurement(2,1,2, time.gmtime(), weight, 'Weight measured')
    lcd.show_ip()
    time.sleep(5)

def create_measurement(deviceID, actionID, userID, time, value, comment):
    data = DataRepository.create_reading(deviceID, actionID, userID, time, value, comment)
    if data is not None:
        return 'ok'
    else:
        return 'error'
      
def gpio_thread():
    setup()
    while True:
        loop()

def callback_button(pin):
    print('button pressed')

def gpio_thread():
    setup()
    while True:
        loop()
        time.sleep(0.01)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)

# API ENDPOINTS

# regio ROUTES
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

ENDPOINT = '/api/v1/waterreminder'

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
        
@app.route(ENDPOINT + '/user/<iduser>/logging/', methods=['GET', 'POST'])
def loggings(iduser):
    if request.method == 'GET':
        pass
        
@app.route(ENDPOINT + '/reminder/<reminderid>/', methods=['GET', 'PUT', 'DELETE'])
def reminder(reminderid):
    if request.method == 'GET':
        reminder = DataRepository.read_one_reminder(reminderid)
        return jsonify(reminder = reminder), 200
    elif request.method == 'PUT':
        form = DataRepository.json_or_formdata(request)
        data = DataRepository.update_reminder(reminderid, form['userid'], form['type'], form['time'], form['amount'], form['fasterWhenHot'])
        if data is not None:
            if data > 0:
                return jsonify(status='OK', data=id), 201
            else:
                return jsonify(status='NO CHANGES'), 200
        else:
            return jsonify(status='ERROR'), 500
    elif request.method == 'DELETE':
        return jsonify(status='DELETED', id=DataRepository.delete_reminder(reminderid))

@app.route(ENDPOINT + '/type/', methods=['GET'])
def types():
    if request.method == 'GET':
        types = DataRepository.read_reminder_types()
        return jsonify(types = types), 200

# regio SOCKETIO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!

@socketio.on('F2B_gettemp')
def show_temp():
    temp = ds18b20.read_temp()
    temp = temp.round()
    print(temp)
    emit('B2F_showtemp', temp)

@socketio.on('F2B_getweight')
def show_weight():
    weight = DataRepository.read_lastweight()
    print(weight)
    emit('B2F_showweight', weight)

@socketio.on('F2B_readrfid')
def show_id():
    iduser = rfid.read_rfid()
    users = DataRepository.read_all_users()
    print(users)
    for user in users:
        ids = []
        ids.append(user['userID'])
        if iduser not in ids:
            emit('B2F_showuser', iduser)
        else:
            emit('B2F_showid', iduser)

@socketio.on('F2B_createuser')
def create_user(payload):
    id = payload['newid']
    name = payload['name']
    goal = payload['goal']
    type = payload['reminderType']
    interval = payload['interval']
    amount = payload['amount']
    print(f'id: {id}, name: {name}, goal: {goal}, type: {type}, interval: {interval}, amount: {amount}')
    if type == 'light':
        typeid = 1
    elif type == 'sound':
        typeid = 2
    elif type == 'vibration':
        typeid = 3
    DataRepository.create_user(id, name, goal, 0)
    DataRepository.create_reminder(id, typeid, interval, amount)

@socketio.on('F2B_getgoal')
def show_goal():
    goal = DataRepository.read_goal_by_userid(2)
    print(goal)
    emit('B2F_showgoal', goal)

if __name__ == '__main__':
    try:
        print("**** Starting APP ****")
        # app.run(debug=False)
        threading.Thread(target=gpio_thread, daemon=True).start()
        # app.run(debug=False)
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        lcd.clear_lcd()
        hx711.cleanup()
        brrr.cleanup()
        leds.cleanup()
        GPIO.cleanup()
        print("finished")
        GPIO.cleanup()