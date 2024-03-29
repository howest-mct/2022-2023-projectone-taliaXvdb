from RPi import GPIO
import time

class DS18B20:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self.sensor_file_name = '/sys/bus/w1/devices/28-23a37a000900/temperature'
        # self.sensor_file_name = '/sys/bus/w1/devices/28-23a37a000900/w1_slave'

    def read_temp(self):
        line = ""
        while line == "":
            sensor_file = open(self.sensor_file_name, 'r')
            line = sensor_file.readline()
            if line:
                line = line.rstrip('\n')
                line = int(line)
                line = format(line/1000, ".0F")
                print(f"De temperatuur is {line} °Celsius")
            sensor_file.close()
        return line