import time

try:
	
	print 'Loading'
	
	while True:
		print '.'
		time.sleep(0.5)

except KeyboardInterrupt:
	print 'Aborted'
