from time import sleep
from RPi import GPIO
import sys
from mfrc522 import SimpleMFRC522


class RFid:
    def __init__(self, io) -> None:
        self.reader = SimpleMFRC522()
        self.socketio = io

    def read_rfid(self):
        print("Hold a tag near the reader")
        self.socketio.sleep(0)
        id = self.reader.read_id()
        print("ID: %s" % (id))
        return id