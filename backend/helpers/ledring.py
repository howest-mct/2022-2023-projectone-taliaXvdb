import time
import board
import neopixel

# Aantal LED's in de ring en GPIO-pinnummer
LED_COUNT = 24
LED_PIN = board.D24

# Maak een Neopixel-object aan
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

# Functie om de LED-ring aan te sturen
def set_led_ring(color):
    for i in range(LED_COUNT):
        pixels[i] = color
        pixels.show()
        time.sleep(0.1)

# Stuur de LED-ring aan met een bepaalde kleur
set_led_ring((255, 0, 0))  # Rood

# Wacht een paar seconden
time.sleep(2)

# Zet alle LED's uit
set_led_ring((0, 0, 0))

# Sluit de Neopixel-objecten af
pixels.deinit()
