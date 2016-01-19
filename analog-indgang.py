# -*- encoding: latin-1 -*-

# Dette program læser analog input fra PCF8591P chipens kanal #0.
from smbus import SMBus
from time import sleep

# Opret forbindelse til enheden(chipen).
bus = SMBus(1) # 1 Indikere at vi bruger enhedsfilen /dev/i2c-1.
# Addressen på chipen.
addresse = 74
# Referencespænding.
Vref = 4.25
konvateret = Vref / 256

print("Læs kanal 0 fra A/D.")
print("Udskriver aflæsningen når den forandres.")
print("Tryk CTRL+C for at stoppe.")

bus.write_byte(addresse, 0) # 0 Indikere at vi vil have data fra kanal 0.
sidste_aflaesning = -1

# Start en uendelig løkke og afbryd hvis ctrl+c bliver trykket.
while True:
	aflaesning = bus.read_byte(addresse)
	if (abs(sidste_aflaesning - aflaesning) > 1 ):
		print "A/D læsning ", aflaesning, " som betyder ", round(konvateret * aflaesning, 2), " V."
		sidste_aflaesning = aflaesning

	sleep(0.01)
