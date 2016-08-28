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
# Den retning robotten sidst drejede. 0 for venstre og 1 for højre.
sidsteRetning = 1
# Standart duty cycle.
stdDC = 40

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Lav en liste indeholdende pins der bruges til mortorne.
motorPins = [11, 12, 15, 16]
# Initialiser en dict til og holde på pwm objekter.
pwm = {}

# Set pin nummerne i "motorPins" til output.
for pin in motorPins:
	GPIO.setup(pin, GPIO.OUT)
	# Sørg for at slukke før vi tænder, så løber robotten ikke væk fra os.
	GPIO.output(pin, 0)
	# Initialiser pwm på "pin" med 50Hz.
	pwm[pin] = GPIO.PWM(pin, 50)
	# Set duty cycle til 0, så løber robotten ikke væk fra os.
	pwm[pin].start(0)

# Lav en liste af tuples til hver operation af motorne.
if True:
	stop = [(11, 0), (12, 0), (15, 0), (16, 0)]
	tilbage = [(12, 1), (15, 1)]
	frem = [(11, 1), (16, 1)]
	hoejre = [(11, 1)]
	venstre = [(16, 1)]
else:
	stop = "stop"
	frem = "frem"
	tilbage = "tilbage"
	hoejre = "højre"
	venstre = "venstre"

def robotDoPWM(pin, tilstand):
	dc = stdDC if tilstand else 0
	pwm[pin].ChangeDutyCycle(dc)

# Send signal til driver ICen L293D om hvilken retning robotten skal tag.
def robotDo(opperationer):
	#print opperationer
	for opperation in opperationer:
		#GPIO.output(*opperation)
		robotDoPWM(*opperation)

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

# Skifter den retning roboten skal søge efter stregen.
# Det vil altid være modsat af den sidste retning.
def nyRetning():
	global sidsteRetning
	if sidsteRetning == 1:
		sidsteRetning = 0
		robotDo(venstre)
	else:
		sidsteRetning = 1
		robotDo(hoejre)

# Genoptager den sidste retning.
def genoptag():
	if sidsteRetning == 1:
		robotDo(hoejre)
	else:
		robotDo(venstre)

# Vi ryder altid op efter os når vi har brugt robotten.
def onExit():
	robotDo(stop)
	# Stop PWM på alle pins.
	for pin in motorPins:
		pwm[pin].stop()
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
		robotDo(hoejre)
		#3 
		while not erPaaStregenH():
			time.sleep(0.01)
		#4
		robotDo(stop)
		#5
		robotDo(venstre)
		#6
		while not erPaaStregenV():
			time.sleep(0.01)
		#7
		robotDo(stop)

#		# Vent på at sensoren er over stregen.
#		while not erPaaStregenV() or erPaaStregenH():
#			if erPaaStregenV():
#				robotDo(hoejre)
#			else
#				robotDo(venstre)
#			genoptag()
#			time.sleep(0.01)
#			robotDo(stop)
#		# Nu er sonsoren over stregen, så vi skal køre frem.
#		robotDo(frem)
#		# Køre fremad så længe sensoren er over stregen.
#		while (erPaaStregen()):
#			time.sleep(0.1)
#		# Sensoren er nu ikke længere over stregen, så skifter vi retning.
#		nyRetning()
		
# Ved Ctrl+C fanges untagelsen "KeyboardInterrupt".
except KeyboardInterrupt:	
	onExit()
finally:
	onExit()

onExit()
