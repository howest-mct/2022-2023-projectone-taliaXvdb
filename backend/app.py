#BACKEND IMPORT
import threading
import time
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
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
from helpers.LCD import LCDClass

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
# lcd = LCDClass([13, 6, 5, 27], 26, 19, 4)
brrr = VibrationMotor(23)
ledring = leds(24, board.D12, 0.1)
hx711.setup()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSCERET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
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
