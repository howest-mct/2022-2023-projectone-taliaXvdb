from RPi import GPIO
import time

class DS18B20:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self.sensor_file_name = '/sys/bus/w1/devices/28-23a37a000900/temperature'

    def read_temp(self):
        sensor_file = open(self.sensor_file_name, 'r')
        for line in sensor_file:
            line = line.rstrip('\n')
            line = int(line)
            print(f"De temperatuur is {line/1000} °Celsius")

        sensor_file.close()