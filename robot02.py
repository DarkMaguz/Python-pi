# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time
import spidev

# Åben SPI bus
spi = spidev.SpiDev()
spi.open(0,1) # Åben port 0, enhed 1.

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Lav en liste indeholdende pins der bruges til mortorne.
motorPins = [11, 12, 15, 16]

# Set pin nummerne i "motorPins" til output.
for pin in motorPins:
	GPIO.setup(pin, GPIO.OUT)
	# Sørg for at slukke før vi tænder.
	GPIO.output(pin, 0)

# Lav en liste af tuples til hver opperation af motorne.
stop = [(11, 0), (12, 0), (15, 0), (16, 0)]
frem = [(12, 1), (15, 1)]
tilbage = [(11, 1), (16, 1)]
hoejre = [(11, 1), (15, 1)]
venstre = [(12, 1), (16, 1)]

def robotDo(opperation):
	for t in opperation:
		GPIO.output(*t)

def onExit():
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()

# Fang untagelser.
try:
	robotDo(stop)
	while (True):
		

# Ved Ctrl+C fanges untagelsen "KeyboardInterrupt".
except KeyboardInterrupt:
	onExit()
finally:
	onExit()

onExit()
