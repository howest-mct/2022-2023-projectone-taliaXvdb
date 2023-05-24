from gewichtssensor import HX711
from temperatuursensor import DS18B20
from trilmotor import VibrationMotor
from ledring import leds
from buzzer import reminder
from LCD import LCDClass
import time
import board
from RPi import GPIO
hx711 = HX711(dt=25, sck=18)
ds18b20 = DS18B20()
buzz = reminder(17, 220)
# lcd = LCDClass([13, 6, 5, 27], 26, 19, 4)
brrr = VibrationMotor(23)
ledring = leds(24, board.D12, 0.1)
hx711.setup()

try:
    while True:
        print("ready")
        weight = hx711.get_weight()
        print("Weight: {} grams".format(weight))
        temp = ds18b20.read_temp()
        ledring.wave_effect(0.05)
        brrr.vibrate(1)
        buzz.reminder_song()
        time.sleep(1)
except KeyboardInterrupt:
    pass

# lcd.clear_lcd()
brrr.cleanup()
hx711.cleanup()
GPIO.cleanup()