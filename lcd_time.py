# Built in libraries
import datetime as dt
import time

# Installed libraries
import Adafruit_CharLCD as LCD


def show_time():
    # Initialise the LCD
    lcd = LCD.Adafruit_CharLCDPlate()
    # Make tuple of string formats
    formatstrings = ('%a %d %b %H:%M', '%a %d %b %H %M')
    while True:
        for formats in formatstrings:
            lcd.set_cursor(0, 1)
            lcd.message(dt.datetime.now().strftime(formats))
            time.sleep(1)

# Test code
if __name__ == '__main__':
    show_time()
