from RPi import GPIO
import time

class reminder:
  def __init__(self, parpin: int, partempo: int) -> None:
      self.pin = parpin
      self.tempo = partempo
      self.quarternote = 1000 / (self.tempo / 60);
      self.setup_buzzer()

  def setup_buzzer(self):
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(self.pin, GPIO.OUT)

  def playForLength(self, hertz, length):
    millisec = 1.0/hertz
    noteStart = time.time()
    while (time.time() - noteStart) < length:
      GPIO.output(self.pin, 1)
      time.sleep(millisec/1.5)
      GPIO.output(self.pin, 0)
      time.sleep(millisec/1.5)

  def reminder_song(self):
    self.playForLength(1046.5, self.quarternote/4)
    self.playForLength(880, self.quarternote/4)
    self.playForLength(698.46, self.quarternote/4)
    time.sleep(self.quarternote/4)
    self.playForLength(1046.5, self.quarternote/4)
    self.playForLength(880, self.quarternote/4)
    self.playForLength(698.46, self.quarternote/4)
    time.sleep(self.quarternote/4)
    self.playForLength(1046.5, self.quarternote/4)
    self.playForLength(880, self.quarternote/4)
    self.playForLength(698.46, self.quarternote/4)
    time.sleep(self.quarternote/4)
    self.playForLength(1046.5, self.quarternote/4)
    self.playForLength(880, self.quarternote/4)
    self.playForLength(698.46, self.quarternote/4)
    time.sleep(self.quarternote/4)