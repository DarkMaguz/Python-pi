# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 18 til output.
GPIO.setup(18, GPIO.OUT)

# Sørg for at slukke før vi tænder.
GPIO.output(18, 0)

# Tænd for LED.
GPIO.output(18, 1)

# Vent i 3 sekunder.
time.sleep(3)

# Nulstil GPIO instilningerne.
GPIO.cleanup()
