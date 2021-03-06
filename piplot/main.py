#!/usr/bin/env python3

import os
import sys
import time
import logging
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
from piplot.config import *
from piplot.menu import menu

###################################################################

GPIO.setwarnings(False)
lcd = CharLCD(pin_rs=LCD_RS, 
            pin_e=LCD_E, 
            pin_rw=None, 
            pins_data=[LCD_DATA4, LCD_DATA5, LCD_DATA6, LCD_DATA7], 
            pin_backlight=None, 
            numbering_mode=GPIO.BCM, 
            cols=NUM_COLS, 
            rows=NUM_ROWS, 
            dotsize=8, 
            charmap='A00')

arrow = (
    0b00000,
    0b10000,
    0b11000,
    0b11100,
    0b11110,
    0b11100,
    0b11000,
    0b10000,
)
tilde = (
    0b00000,
    0b00000,
    0b00000,
    0b01101,
    0b10101,
    0b10110,
    0b00000,
    0b00000,
)
lcd.create_char(0, arrow)
lcd.create_char(1, tilde)
menu = menu(lcd,
            cols=NUM_COLS, 
            rows=NUM_ROWS,
            pycnc=PYCNC_EXEC,
            gcode_path=GCODE_REPO)

def pg_up_cb(channel):
    ''' page up button callback '''
    if GPIO.input(channel) == GPIO.HIGH:
        menu.set_up()

def pg_down_cb(channel):
    ''' page down button callback '''
    if GPIO.input(channel) == GPIO.HIGH:
        menu.set_down()

def pg_ok_cb(channel):
    ''' page ok button callback '''
    if GPIO.input(channel) == GPIO.HIGH:
        menu.set_ok()

def init():
    ''' init pins and display main menu '''
    if not os.path.exists(GCODE_REPO):
        logging.error("Path {} doesn't exist".format(GCODE_REPO))
        sys.exit(1)

    try:
        GPIO.setup(PG_UP, GPIO.IN)
        GPIO.setup(PG_DOWN, GPIO.IN)
        GPIO.setup(PG_OK, GPIO.IN)
        GPIO.add_event_detect(PG_UP, GPIO.RISING, callback=pg_up_cb, bouncetime=50)
        GPIO.add_event_detect(PG_DOWN, GPIO.RISING, callback=pg_down_cb, bouncetime=50)
        GPIO.add_event_detect(PG_OK, GPIO.RISING, callback=pg_ok_cb, bouncetime=50)
    except:
        e = sys.exc_info()[1]
        logging.error("Error : {}".format(e))
        sys.exit(1)
    menu.init_menu()

def main():
    logging.basicConfig(filename='/var/log/PiPlot2D.log', level=logging.INFO)
    logging.info("*** Launch PiPlot2D Menu & Control ***")
    init()
    while True:
        time.sleep(1)
    logging.info("*** Exit PiPlot2D Menu & Control ***")
    lcd.close()

###################################################################

if __name__ == '__main__':
    main()

