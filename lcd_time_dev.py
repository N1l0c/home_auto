# Built in libraries
import datetime as dt
import time

# Installed libraries
import Adafruit_CharLCD as LCD

# Initialise the LCD
lcd = LCD.Adafruit_CharLCDPlate()
datetime_strings = ('%a %d %b %H:%M', '%a %d %b %H %M')
time_strings = ('%H:%M', '%H %M')


def show_time24(position='top right'):
    # Split the argument into components
    arguments = str.split(position)
    row_string = arguments[0]
    col_string = arguments[1]
    # Set the relevant cursor positions
    if row_string == 'bottom':
        row = 1
    else:
        row = 0

    if col_string == 'left':
        col = 0
    else:
        col = 11

    while True:
        for formats in time_strings:
            lcd.set_cursor(col, row)
            lcd.message(dt.datetime.now().strftime(formats))
            time.sleep(1)

def show_datetime():
    # Make tuple of string formats
    while True:
        for formats in datetime_strings:
            lcd.set_cursor(0, 1)
            lcd.message(dt.datetime.now().strftime(formats))
            time.sleep(1)

# Test code
if __name__ == '__main__':
    show_time24()
