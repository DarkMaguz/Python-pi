# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time
import curses

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

#######################
# Initialiser curses. #
#######################
stdscr = curses.initscr()
cursesIsRunning = True

# Udskriv ikke tastetryk automatisk til skærmen.
curses.noecho()

# Vi vil gerne have at programmet skal reagere med det samme vi trykker på en tast,
# så vi ikke behøver og trykke enter hver gang.
curses.cbreak()

# Bed curses om at fortolke specielle taster, f.eks. piltast op fortolkes som curses.KEY_UP.
stdscr.keypad(1)

# Skriv noget oppe i venstre hjørne.
stdscr.addstr(0,0,"Brug ""w"", ""s"", ""a"", ""d"" eller piltasterne til og styre robotten.")
stdscr.refresh()

# Skriv noget nede i venstre side.
stdscr.addstr(20,0,"Tryk 'q' eller Ctrl+C for at afslutte.")
stdscr.refresh()

# Skriv noget i midten af skrmen.
stdscr.addstr(9, 20, "Op")
stdscr.addstr(11, 20, "Ned")
stdscr.addstr(10, 11, "Venstre")
stdscr.addstr(10, 25, "Højre")
stdscr.addstr(6, 19, "Stop")

def onExit():
	global cursesIsRunning
	if cursesIsRunning == True:
		# Deinitialiser curses.
		curses.nocbreak(); stdscr.keypad(0); curses.echo()
		curses.endwin()
		cursesIsRunning = False
		# Nulstil GPIO instilningerne.
		GPIO.cleanup()
	else:
		print("onExit() har kørt før.")

# Fang untagelser.
try:
	key = ''
	while key != ord('q'):
		key = stdscr.getch()
		#stdscr.addstr(19,0,chr(key) + " ")
		stdscr.refresh()
		robotDo(stop)
		#time.sleep(0.3)
		if key == curses.KEY_UP or key == ord('w'):
			stdscr.addstr(9, 20, "Op")
			robotDo(frem)
		elif key == curses.KEY_DOWN or key == ord('s'):
			stdscr.addstr(11, 20, "Ned")
			robotDo(tilbage)
		elif key == curses.KEY_LEFT or key == ord('a'):
			stdscr.addstr(10, 11, "Venstre")
			robotDo(venstre)
		elif key == curses.KEY_RIGHT or key == ord('d'):
			stdscr.addstr(10, 25, "Højre")
			robotDo(hoejre)
		else:
			stdscr.addstr(6, 19, "Stop")

# Ved Ctrl+C fanges untagelsen "KeyboardInterrupt".
except KeyboardInterrupt:
	onExit()
finally:
	onExit()

onExit()
