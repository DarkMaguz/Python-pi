# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time
import spidev

# Initialiser et ny spi objekt.
spi = spidev.SpiDev()
# Forbinder til den specifikke SPI enhed, ved "/dev/spidev0.0".
spi.open(0, 0) # Åben port 0, enhed 0.

# Set grænseværdien for hvornår vi med stor sandsynlighed kan sige at vi er på en streg.
graenseVaerdi = 50

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Lav en liste indeholdende pins der bruges til mortorne.
motorPins = [11, 12, 15, 16]

# Set pin nummerne i "motorPins" til output.
for pin in motorPins:
	GPIO.setup(pin, GPIO.OUT)
	# Sørg for at slukke før vi tænder, så løber robotten ikke væk fra os.
	GPIO.output(pin, 0)

# Lav en liste af tuples til hver operation af motorne.
stop = [(11, 0), (12, 0), (15, 0), (16, 0)]
tilbage = [(12, 1), (15, 1)]
frem = [(11, 1), (16, 1)]
hoejre = [(16, 1)]
venstre = [(11, 1)]

# Send signal til driver ICen L293D om hvilken retning robotten skal tag.
def robotDo(opperationer):
	for opperation in opperationer:
		GPIO.output(*opperation)

# Hent SPI data fra MCP3008 chippen.
def hentData(kanal):
        adc = spi.xfer2([1,(8+kanal)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Retuner "true" hvis stregen er under den højre sensor ellers retuneres "false".
def erPaaStregenH():
	return hentData(1) > graenseVaerdi

# Retuner "true" hvis stregen er under den venstre sensor ellers retuneres "false".
def erPaaStregenV():
	return hentData(0) > graenseVaerdi

# Vi ryder altid op efter os når vi har brugt robotten.
def onExit():
	robotDo(stop)
	# Sluk for alle pins.
	for pin in motorPins:
		GPIO.output(pin, 0)
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()

# Eksekveringsbeskrivelse(user story):
# 1) Robotten placeres på stregen mellem de 2 IR moduler.
# 2) Start det højre hjul i fremadgående retning.
# 3) Vent på at højre sensor kommer over stregen.
# 4) Stop.
# 5) Start det venstre hjul i fremadgående retning.
# 6) Vent på at venstre sensor kommer over stregen.
# 7) Stop.
# 8) Gentag fra #2.

# Fang untagelser.
try:
	#1
	while True:
		#2
		print "#2"
		robotDo(hoejre)
		#3
		print "#3"
		while not erPaaStregenH():
			time.sleep(0.01)
		#4
		print "#4"
		robotDo(stop)
		#5
		print "#5"
		robotDo(venstre)
		#6
		print "#6"
		while not erPaaStregenV():
			time.sleep(0.01)
		#7
		print "#7"
		robotDo(stop)

# Ved Ctrl+C fanges untagelsen "KeyboardInterrupt".
except KeyboardInterrupt:
	onExit()
finally:
	onExit()

onExit()
