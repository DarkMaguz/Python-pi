# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
from time import sleep
import random

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Definer et loft for antalet af gæt vi skal gætte rigtigt for at vinde.
maxGaet = 30
# Definer hvor mange fejl vi max må få før vi taber.
maxFejl = 3

# Et array med de GPIO nummer der er forbundet til knapper.
knapper = [18, 23, 24, 25]
# Et array med de GPIO nummer der er forbundet til LEDs.
lamper = [4, 17, 27, 22]
# Et array med farverne i den rækkefølge de er stillet på bordet.
farver = ["rød", "grøn", "gul", "blå"]

# Set GPIO pin's i arrayet "knapper" til input.
for pin in knapper:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set GPIO pin's i arrayet "lamper" til output.
for pin in lamper:
	GPIO.setup(pin, GPIO.OUT)
	# Sørg for at alle lamperne er slukket til og starte med.
	GPIO.output(pin, 0)

def skrivRaekkefoelge(fremskridt, randomTal):
	for i in range(0, fremskridt):
		# Tænd for LED.
		GPIO.output(lamper[randomTal[i]], 1)
		#print i, " ", randomTal[i], " ", lamper[randomTal[i]]
		sleep(1)
		# Sluk for den samme LED som vi lige har tændt.
		GPIO.output(lamper[randomTal[i]], 0)
		sleep(0.3)

def modtagTryk():
	while True:
		for i in range(0, 4):
			if GPIO.input(knapper[i]) == 0:
				# Tænd for den tilsvarende LED som knappen der bliver trykket på.
				GPIO.output(lamper[i], 1)
				sleep(0.05)
				# Loop så længe knappen holdes nede.
				while GPIO.input(knapper[i]) == 0:
					sleep(0.05)
				# Sluk for LEDen igen.
				GPIO.output(lamper[i], 0)
				# Returner den knap som blev trykket på.
				return i

def modtagRaekkefoelge(fremskridt, randomTal):
	print "Nu skal du abe efter..."
	for trykNummer in range(0, fremskridt):
		forsoeg = modtagTryk()
		print "Du trykkede: ", farver[forsoeg], " jeg forventede ", farver[randomTal[trykNummer]]
		if forsoeg != randomTal[trykNummer]:
			sleep(0.5)
			# Returner False hvis vi gætter forkert.
			return False
	# Returner True hvis vi gætter rigtigt.
	return True

try:
	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
		# Vi har 0 fejl til at begynde med.
		fejl = 0
		# Vi starter med 2 farver der skal gættes.
		fremskridt = 2
		# Generer et talrække med tilfældige tal fra 0 til 3.
		randomTal = [ random.randint(0, 3) for r in range(0, maxGaet) ]
		# Begynd et nyt spil.
		while fejl < maxFejl:
			print "Se efter hvilken rækkefølge jeg tænder de næste ", fremskridt, " lamper..."
			skrivRaekkefoelge(fremskridt, randomTal)
			if modtagRaekkefoelge(fremskridt, randomTal):
				fremskridt = fremskridt + 1
				print "Det var godt lille abe - prøv en længere rækkefølge."
				# Nulstil fejl tælleren.
				fejl = 0
			else:
				fejl = fejl + 1
				print "Fejl nummer ", fejl, "."
				if fejl < maxFejl:
					print "Det må du prøve og gøre bedre."
			sleep(1)
			if fremskridt > maxGaet:
				print "Tillykke! du har gennemført spillet."
				print "Sikke en dygtig lille abekat du er :)"
				exit()
		print "Spillet er slut - du nåede til niveau", fremskridt - 1, "."
		print "Prøv igen!"
		sleep(1)

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
