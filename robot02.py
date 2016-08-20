# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time
import spidev

#Initialiser et ny spi objekt.
spi = spidev.SpiDev()
#Forbinder til den specifikke SPI enhed, ved "/dev/spidev0.0".
spi.open(0, 0) # Åben port 0, enhed 0.

# Set grænseværdien for hvornår vi med stor sandsynlighed kan sige at vi er på en streg.
graenseVaerdi = 50
# Den retning robotten sidst drejede. 0 for venstre og 1 for højre.
sidsteRetning = 1

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
if True:
	stop = [(11, 0), (12, 0), (15, 0), (16, 0)]
	tilbage = [(12, 1), (15, 1)]
	frem = [(11, 1), (16, 1)]
	hoejre = [(11, 1), (15, 1)]
	venstre = [(12, 1), (16, 1)]
else:
	stop = "stop"
	frem = "frem"
	tilbage = "tilbage"
	hoejre = "højre"
	venstre = "venstre"


# Send signal til driver ICen L293D om hvilken retning robotten skal tag.
def robotDo(opperation):
	#print opperation
	for t in opperation:
		GPIO.output(*t)

# Hent SPI data fra MCP3008 chippen.
def hentData(kanal):
        adc = spi.xfer2([1,(8+kanal)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

# Retuner "true" hvis sensoren er over stregen ellers retuneres "false".
def erPaaStregen():
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


def onExit():
	robotDo(stop)
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()

# Eksekveringsbeskrivelse:
# 1) Drej til højre indtil stregen er under sensoren.
# 2) Kør ligeud så længe stregen er under under sensoren.
# 3) Hvis stregen forsvinder under sensoren, så drej i modsat retning af den forrige retning. 
# 4) Gentag 2 - 3. 

# Fang untagelser.
try:
	robotDo(hoejre)
	while True:
		# Vent på at sensoren er over stregen.
		while not erPaaStregen():
			genoptag()
			time.sleep(0.01)
			robotDo(stop)
		# Nu er sonsoren over stregen, så vi skal køre frem.
		robotDo(frem)
		# Køre fremad så længe sensoren er over stregen.
		while (erPaaStregen()):
			time.sleep(0.1)
		# Sensoren er nu ikke længere over stregen, så skifter vi retning.
		nyRetning()
		
# Ved Ctrl+C fanges untagelsen "KeyboardInterrupt".
except KeyboardInterrupt:	
	onExit()
finally:
	onExit()

onExit()
