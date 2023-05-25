from RPi import GPIO
import time

class reminder:
  def __init__(self, parpin: int) -> None:
      self.pin = parpin
      self.quarternote = 0.25
      self.setup_buzzer()

  def setup_buzzer(self):
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(self.pin, GPIO.OUT)

  def buzz(self, noteFreq, duration):
      halveWaveTime = 1 / (noteFreq * 2 )
      waves = int(duration * noteFreq)
      for i in range(waves):
        GPIO.output(self.pin, True)
        time.sleep(halveWaveTime)
        GPIO.output(self.pin, False)
        time.sleep(halveWaveTime)

  def reminder_song(self):
    t = 0
    notes=[1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 987.77, 783.99, 659.25, 987.77, 783.99, 659.25, 987.77, 783.99, 1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 1046.5, 880, 698.46, 0.01, 987.77, 783.99, 659.25, 987.77, 783.99, 880, 783.99, 1046.50]
    duration=[self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote/2, self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote,self.quarternote]
    for n in notes:
        self.buzz(n, duration[t])
        time.sleep(duration[t] *0.1)
        if t in [3,7,11,15,27,31,35,39]:
           time.sleep(self.quarternote/2)
        t+=1
