import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def buildReadCommand(channel):
	startBit = 0x01
	singleEnded = 0x08

	return [startBit, singleEnded|(channel<<4), 0]

def processAdcValue(result):
	'''Take in result as array of three bytes. 
		Return the two lowest bits of the 2nd byte and
		all of the third byte'''
	byte2 = (result[1] & 0x03)
	return (byte2 << 8) | result[2]

def readAdc(channel):
	if ((channel > 7) or (channel < 0)):
		return -1
	r = spi.xfer2(buildReadCommand(channel))
	return processAdcValue(r)

if __name__ == '__main__':
<<<<<<< HEAD
	try:
		while True:
			val = readAdc(0)
			print "ADC Result: ", str(val)
			sleep(0.1)
	except KeyboardInterrupt:
		spi.close()
=======
    try:
        while True:
            val = readAdc(0)
            print "ADC Result: ", str(val)
            time.sleep(0.1)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
>>>>>>> 3cf95b9c71c97adbda0150c222c730e41119fec1
