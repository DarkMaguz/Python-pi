# -*- encoding: latin-1 -*-
import spidev
import time

#Initialiser et ny spi objekt.
spi = spidev.SpiDev()

#Forbinder til den specifikke SPI enhed, ved "/dev/spidev0.0".
spi.open(0, 0)

#Hent SPI data fra MCP3008 chippen.
def hentData(kanal):
	adc = spi.xfer2([1,(8+kanal)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

#Fang "ctrl+c".
try:
	while True:
		adcVaerdi = hentData(0)
		print "ADC Værdi:", str(adcVaerdi)
		time.sleep(0.1)
except KeyboardInterrupt:
	#Efter "ctrl+c", lukker vi forbindelses til SPI enheden.
	spi.close();
