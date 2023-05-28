import time
import neopixel

class leds:
    def __init__(self, parcount, parpin, parbright: float) -> None:
        self.count = parcount
        self.pin = parpin
        self.brightness = parbright

        self.setup()

    def setup(self):
        self.pixels = neopixel.NeoPixel(self.pin, self.count)
        self.pixels.brightness = self.brightness

    def rainbow_effect(self, wait):
        for i in range(self.count):
            hue = int(i * (255 / self.count))
            self.pixels[i] = (hue, 255 - hue, 0)
        self.pixels.show()
        time.sleep(wait)

    def wave_effect(self, wait):
        for i in range(self.count):
            self.pixels.fill((0, 0, 0))  # Zet alle leds uit
            self.pixels[i] = (0, 0, 255)  # Schakel de huidige led in
            self.pixels.show()
            time.sleep(wait)