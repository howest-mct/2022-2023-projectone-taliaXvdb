from time import sleep
from RPi import GPIO
import sys
from mfrc522 import SimpleMFRC522


class RFid:
    def __init__(self) -> None:
        self.reader = SimpleMFRC522()

    def read_rfid(self):
        print("Hold a tag near the reader")
        id, text = self.reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)