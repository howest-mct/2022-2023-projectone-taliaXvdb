#BACKEND IMPORT
import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import datetime

#GPIO IMPORT
from RPi import GPIO
import time
import datetime
import pytz
import board
from helpers.gewichtssensor import HX711
from helpers.temperatuursensor import DS18B20
from helpers.trilmotor import VibrationMotor
from helpers.ledring import leds
from helpers.buzzer import reminder
from helpers.LCD import LCDpcfClass
from helpers.rfid import RFid
from helpers.klasseknop import Button
import subprocess

#REGION GPIO, PIN DEFINING, GLOBAL VAR
btn = Button(21)
lcdPins = {
    'rs': 26,
    'e': 19
}

weightPins = {
    'dt': 25,
    'sck': 18
}

UserID = 0
login = False
prevTemp = 0
prevWeight = 0
scanned = False
goal = 0
startweight = 0
totalDrank = 0
noitsnull = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5) #, async_handlers=False
CORS(app)

hx711 = HX711(weightPins['dt'], weightPins['sck'])
ds18b20 = DS18B20()
buzz = reminder(16)
lcd = LCDpcfClass(lcdPins['rs'], lcdPins['e'])
brrr = VibrationMotor(23)
ledring = leds(24, board.D12, 0.1)
rfid = RFid(socketio)

def setup():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(btn, GPIO.IN)
    # GPIO.add_event_detect(btn, GPIO.FALLING, callback=callback_button, bouncetime=300)
    lcd.set_cursor()
    lcd.clear_lcd()
    print("hx711 setup begin")
    hx711.setup()
    print("hx711 setup done")
    lcd.show_ip()
    btn.on_press(shutdown)
    shutdown(btn)

def loop():
    global UserID, login, prevTemp, prevWeight, scanned, goal, startweight, totalDrank, noitsnull
    if login == True:
        start_time = time.time()
        elapsed_time = 0
        utc_time = datetime.datetime.utcnow()
        desired_timezone = pytz.timezone('Europe/Brussels')
        interval = get_interval(UserID)
        while noitsnull == True:
            while startweight <= 0:
                socketio.emit('B2F_placedrink', interval)
                time.sleep(3)
                startweight = hx711.get_weight()
                if startweight > 0:
                    noitsnull = False
                    socketio.emit('B2F_closepopup')
        totalDrank = DataRepository.read_loggedwater_by_userid(UserID)
        totalDrank = totalDrank[0]['total']
        if totalDrank == None:
            totalDrank = 0
        while True:
            interval = get_interval(UserID)
            temp = ds18b20.read_temp()
            socketio.emit('B2F_showtemp', temp)
            weight = round(hx711.get_weight())
            if temp != prevTemp:
                create_measurement(1,1, UserID, utc_time.replace(tzinfo=pytz.utc).astimezone(desired_timezone), temp, 'Temperature measured')
                prevTemp = temp
            
            if weight != prevWeight:
                if weight > 0:
                    create_measurement(2,1,UserID, utc_time.replace(tzinfo=pytz.utc).astimezone(desired_timezone), weight, 'Weight measured')
                    prevWeight = weight
                else:
                    pass

            current_time = time.time()
            elapsed_time = current_time - start_time

            remaining_time = interval - elapsed_time
            print("Resterende tijd:", remaining_time, "seconden")
            socketio.emit('B2F_showremaining', remaining_time)
            
            time.sleep(1)


            if elapsed_time > interval:
                scanned = False
                doReminder(UserID)
                print("Timer afgelopen!")
                userid = rfid.read_rfid()
                if userid == UserID:
                    newestweight = hx711.get_weight()
                    print(newestweight)
                    drank = round(startweight - newestweight)
                    print(startweight)
                    print(drank)
                    if drank < 0:
                        drank = 0
                    totalDrank += drank
                    datetimed = str(datetime.datetime.now())
                    if totalDrank == goal:
                        create_logged(UserID, datetimed, drank, 1)
                    else:
                        create_logged(UserID, datetimed, drank, 0)
                    
                    print(totalDrank)
                    socketio.emit('B2F_showprogress', int(totalDrank))
                    start_time = time.time()
        
def create_measurement(deviceID, actionID, userID, time, value, comment):
    data = DataRepository.create_reading(deviceID, actionID, userID, time, value, comment)
    if data is not None:
        return 'ok'
    else:
        return 'error'
    
def create_logged(userid, datetimed, amount, reached):
    date, time = datetimed.split(' ')
    data = DataRepository.create_logging(userid, date, time, amount, reached)
    if data is not None:
        return 'ok'
    else:
        return 'error'

def callback_button(pin):
    print('button pressed')

def shutdown(channel):
    if btn.pressed:
        print('shutdown')
        subprocess.call(['sudo', 'shutdown', 'now'])

def gpio_thread():
    setup()
    while True:
        loop()
        time.sleep(0.01)

def get_interval(userid):
    intervalreminder = DataRepository.read_intervalreminder_by_userid(userid)
    print(intervalreminder[0]['time'])
    interval = intervalreminder[0]['time']
    interval = interval*60


    return interval

def doReminder(userid):
    global scanned
    type = DataRepository.read_remindertype_by_userid(userid)
    print('reminder', type[0]["type"])
    while scanned != True:
        userid = rfid.reader.read_id_no_block()
        print("RFIDDD", userid)
        if userid:
            scanned = True
        else:
            if type[0]["type"] == 1:
                print("yes")
                ledring.wave_effect(0.2)

            elif type[0]["type"] == 2:
                buzz.reminder_song()

            elif type[0]["type"] == 3:
                brrr.vibrate(5)

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
        
@app.route(ENDPOINT + '/user/<iduser>/temperature/', methods=['GET'])
def temperature(iduser):
    if request.method == 'GET':
        result = DataRepository.read_temperature(iduser)
        return jsonify(data=result), 200
    
@app.route(ENDPOINT + '/user/<iduser>/weight/', methods=['GET'])
def weight(iduser):
    if request.method == 'GET':
        result = DataRepository.read_weight(iduser)
        return jsonify(data=result), 200
    
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
        
@app.route(ENDPOINT + '/user/<iduser>/logging/', methods=['GET'])
def total(iduser):
    if request.method == 'GET':
        progress = DataRepository.read_loggedwater_by_userid(iduser)
        return jsonify(progress=progress), 200

@app.route(ENDPOINT + '/user/<iduser>/logging/last/', methods=['GET'])
def last_logging(iduser):
    if request.method == 'GET':
        user = DataRepository.read_user(iduser)
        last_log = DataRepository.read_lastlogging_by_userid(iduser)
        return jsonify(user=user, data=last_log), 200
        
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

@socketio.on('F2B_poweroff')
def poweroff():
    subprocess.call(['sudo', 'shutdown', 'now'])

@socketio.on('F2B_gettemp')
def show_temp():
    temp = ds18b20.read_temp()
    print(temp)
    emit('B2F_showtemp', temp)

@socketio.on('F2B_getweight')
def show_weight():
    weight = DataRepository.read_lastweight()
    print(weight)
    emit('B2F_showweight', weight)

@socketio.on('F2B_readrfid')
def show_id():
    global UserID, login, goal, startweight
    iduser = rfid.read_rfid()
    users = DataRepository.read_all_users()
    UserID = iduser
    for user in users:
        ids = []
        ids.append(user['userID'])
        if iduser not in ids:
            emit('B2F_showuser', iduser)
        else:
            emit('B2F_showid', iduser)
            goal = DataRepository.read_goal_by_userid(iduser)
            startweight = hx711.get_weight()
            login = True

@socketio.on('F2B_createuser')
def create_user(payload):
    global login
    id = payload['newid']
    name = payload['name']
    goal = payload['goal']
    type = payload['reminderType']
    interval = payload['interval']
    amount = payload['amount']
    print(f'id: {id}, name: {name}, goal: {goal}, type: {type}, interval: {interval}, amount: {amount}')
    if type == 'light':
        typeid = 1
        notid = [2,3]
    elif type == 'sound':
        typeid = 2
        notid = [1,3]
    elif type == 'vibration':
        typeid = 3
        notid = [2,1]

    DataRepository.create_user(id, name, goal, 0)
    DataRepository.create_reminder(id, typeid, interval, amount)
    for falseid in notid:
        DataRepository.create_reminder(id, falseid, 0, 0)
    login = True

@socketio.on('F2B_getgoal')
def show_goal():
    global UserID
    goal = DataRepository.read_goal_by_userid(UserID)
    print(goal)
    emit('B2F_showgoal', goal)

@socketio.on('F2B_lighton')
def light_on():
    ledring.wave_effect(0.1)
    time.sleep(1)

@socketio.on('F2B_playmusic')
def sound_on():
    buzz.reminder_song()
    time.sleep(3)

@socketio.on('F2B_vibrate')
def vibrate_on():
    brrr.vibrate(3)
    time.sleep(1)

@socketio.on('F2B_updatereminder')
def update_reminder(payload):
    reminderid = payload[0]
    userid = payload[1]
    type = payload[2]
    time = payload[3]
    amount = payload[4]
    DataRepository.update_reminder(reminderid, userid, type, time, amount)


@socketio.on('F2B_updateuser')
def update_user(payload):
    userid = payload[0]
    name = payload[1]
    goal = payload[2]
    streak = payload[3]
    DataRepository.update_user(userid, name, goal, streak)

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
        ledring.cleanup()
        lcd.clear_lcd()
        hx711.cleanup()
        brrr.cleanup()
        GPIO.cleanup()
        print("finished")
        GPIO.cleanup()