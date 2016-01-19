#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ping-pong v2 (uses a IC 4511 for each 7 segments display).
This is a ping-pong look-alike but the maximum score is 9 instead of 11 due to
the use of only one 7 segment display per player.
To run it just copy this file to your home directory (usually /home/pi) and
execute the following command in the Raspberry command line
sudo python ~/ping-pongv1.py

Rules:
A point is won when the other player is unable to press the button on time to
send the “ball” (lit LED) to the other side or if the other player presses the
button in advance.
The player who wins the point starts the next service.
A game is won after 9 points.
A match should consist of any odd number of games (usually five or seven).

For the first service, the starting player is randomly selected.
The time between LED jumps is random to make it more difficult to predict.
The buzzer will sound every time a point is won.

This program uses board pins numbering system.
"""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import time

import RPi.GPIO as GPIO


BUTTON_1 = 7
BUTTON_2 = 40
IN = [BUTTON_1, BUTTON_2]  # all input pins

LEDS = [16, 18, 22, 29, 31, 32]
BUZZER = 33

DISPLAY_1 = [15, 13, 12, 11]  # IC 4511 D, C, B, A
DISPLAY_2 = [38, 37, 36, 35]  # IC 4511 D, C, B, A
DIGITS_MASKS = {0: [0, 0, 0, 0], 1: [0, 0, 0, 1], 2: [0, 0, 1, 0],
                3: [0, 0, 1, 1], 4: [0, 1, 0, 0], 5: [0, 1, 0, 1],
                6: [0, 1, 1, 0], 7: [0, 1, 1, 1], 8: [1, 0, 0, 0],
                9: [1, 0, 0, 1]}

OUT = LEDS + [BUZZER] + DISPLAY_1 + DISPLAY_2  # all output pins

# "ball" direction
RIGHT = 1
LEFT = -1

# "ball" position limits
FIRST = 0
LAST = len(LEDS) - 1

MAX_SCORE = 9

# global score vars
player_1 = 0
player_2 = 0


def set_in_pins(pins):
    """Setup input pins."""
    for pin in pins:
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)  # activates pull down resistor


def set_out_pins(pins):
    """Setup output pins."""
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)


def pin_low(pin):
    """Activates low (0 volts / GND) signal on specified pin."""
    GPIO.output(pin, GPIO.LOW)


def all_low(pins_lst):
    """Activates low (0 volts / GND) signal on all pins on the list."""
    for pin in pins_lst:
        pin_low(pin)


def all_high(pins_lst):
    """Activates high (3.3v) signal on all pins on the list."""
    for pin in pins_lst:
        pin_high(pin)


def set_pins_signals(pins, signals, pause=0):
    """Activates signals on pins."""
    GPIO.output(pins, signals)
    time.sleep(pause)


def show_digit(digit=0, display=DISPLAY_1):
    """Show digit in specififed display."""
    set_pins_signals(display, DIGITS_MASKS[digit])


def show_scores():
    """Shows players scores."""
    show_digit(player_1, DISPLAY_1)  # show player 1 score on 1st display
    show_digit(player_2, DISPLAY_2)  # show player 2 score on 2nd display


def pin_high(pin):
    """Activates high (3.3v) signal on specified pin."""
    GPIO.output(pin, GPIO.HIGH)


def led_on(pos):
    """Switch LED on and pauses."""
    pin_high(LEDS[pos])
    if pos in [FIRST, LAST]:  # 1st or last LED
        pause = 0.4  # fixed delay to allow button response
    else:
        pause = 0.5 #random.choice([0.5, 1, 1.5, 2])  # random delay
    time.sleep(pause)


def led_off(pos):
    """Switch LED off."""
    pin_low(LEDS[pos])


def is_on(pin):
    """True if pin has a high signal."""
    return GPIO.input(pin) == GPIO.HIGH


def buzzer(pin, pause=1):
    """Activates buzzer."""
    pin_high(pin)
    time.sleep(pause)
    pin_low(pin)


def end_service():
    """Buzzes and updates scores."""
    buzzer(BUZZER)
    show_scores()
    time.sleep(2)


def out_sequence(pause=1):
    """Shows LED sequence from inside out."""
    nr_leds = len(LEDS)
    for pos in range(nr_leds // 2, 0, -1):  # reverse order
        # activate pair
        pin_high(LEDS[pos - 1])
        pin_high(LEDS[-pos + nr_leds])

        time.sleep(pause)

        # deactivate pair
        pin_low(LEDS[pos - 1])
        pin_low(LEDS[-pos + nr_leds])
    time.sleep(pause)


try:
    GPIO.setmode(GPIO.BOARD)  # setup pin numbering system
    GPIO.setwarnings(False)

    set_in_pins(IN)  # setup input pins
    set_out_pins(OUT)  # setup output pins

    all_low(OUT)  # clear all output pins
    all_high(DISPLAY_1 + DISPLAY_2)  # IC 4511 clears with a high signal

    cur_pos = random.choice([FIRST, LAST])  # define 1st LED to be lit
    if cur_pos == FIRST:
        direction = RIGHT
    else:
        direction = LEFT

    buzzer(BUZZER)
    show_scores()

    while player_1 < MAX_SCORE and player_2 < MAX_SCORE:
        # light LED (ball) and pause for a little time to allow the players to
        # press the button
        led_on(cur_pos)

        led_off(cur_pos)

        if ((direction == RIGHT and cur_pos < LAST) or  # not in last position
            (direction == LEFT and cur_pos > FIRST)):  # not in first position

            if is_on(BUTTON_1):  # if button 1 was pressed player 1 loses
                player_2 += 1
                cur_pos = LAST
                direction = LEFT
                end_service()
            elif is_on(BUTTON_2):  # if button 2 was pressed player 2 loses
                player_1 += 1
                cur_pos = FIRST
                direction = RIGHT
                end_service()
            else:
                cur_pos += direction  # updates position

        else:  # it is the first or last position

            if ((cur_pos == LAST and is_on(BUTTON_2)) or
                (cur_pos == FIRST and is_on(BUTTON_1))):

                direction *= -1  # change direction
                cur_pos += direction

            else:  # player didn't push button on time

                if cur_pos == FIRST:  # player 1 loses
                    player_2 += 1
                    cur_pos = LAST
                    direction = LEFT
                else:  # player 2 loses
                    player_1 += 1
                    cur_pos = FIRST
                    direction = RIGHT
                end_service()

    out_sequence()

except KeyboardInterrupt as error:
    pass

finally:  # always executed
    GPIO.cleanup()  # restores all pins to pre-game state

