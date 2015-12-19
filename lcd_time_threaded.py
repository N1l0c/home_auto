# Built in libraries
import threading
import datetime as dt
import time

# Installed libraries
import Adafruit_CharLCD as LCD

class TimeDisplay(object):

    def __init__(self, display):
        self.lcd = display

        thread = threading.Thread(target=self.show_time())
        thread.daemon = True
        thread.start()

    def show_time(self):
        # Make tuple of string formats
        formatstrings = ('%a %d %b %H:%M', '%a %d %b %H %M')
        while True:
            for formats in formatstrings:
                self.lcd.set_cursor(0, 1)
                self.lcd.message(dt.datetime.now().strftime(formats))
                time.sleep(1)

# Test code
if __name__=='__main__':
    TimeDisplay(LCD.Adafruit_CharLCDPlate())

