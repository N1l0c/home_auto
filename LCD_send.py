import time
import datetime as dt
import Queue
import threading

import Adafruit_CharLCD as LCD


##############################

class Display(object):
    """
    This class contains all the functionality used to control an LCD specifically
    for the home_auto system

    Passthrough functions are provided from the Adafruit_Char LCD library
    """
    # LCD setup and functions
    lcd = LCD.Adafruit_CharLCDPlate()
    backlight_status = True

    # Custom characters
    lcd.create_char(0, [24, 24, 3, 4, 4, 4, 3, 0])  # Create a degrees character
    lcd.create_char(1, [4, 14, 21, 4, 4, 0, 0, 0])  # Up arrow
    lcd.create_char(2, [0, 0, 4, 4, 21, 14, 4, 0])  # Down arrow
    lcd.create_char(3, [4, 4, 4, 4, 4, 4, 4, 4])    # Separator pipe

    # Hex values for custom characters
    degrees = '\x00'
    arrows_up = '\x01\x01\x01'
    arrows_down = '\x02\x02\x02'
    pipe = '\x03'

    # String formats for printing
    datetime_strings = ('%a %d %b %H:%M', '%a %d %b %H %M')
    time_strings = (pipe + '%H:%M', pipe + '%H %M')

    # Buttons
    left = LCD.LEFT
    right = LCD.RIGHT
    up = LCD.UP
    down = LCD.DOWN
    select = LCD.SELECT

    lcd_queue = Queue.Queue()

    def __init__(self):
        """ Constructor
        :return: Object that controls LCD display
        :param lcd_queue: Queue for message sending to LCD
        :type lcd_queue: Queue.Queue()
        """

        self.tick = False    # Tick counter for clock

        threading.Thread(target=self._send_message, args=()).start()

    #################################################################
    def _add_to_queue(self, text, row=1, alignment=left):
        """

        :param message_tuple: Tuple containing message string, row and alignment
        :return:
        """
        Display.lcd_queue.put((text, row))

    def _send_message(self):
        # Get message parameters from Queue and send message to lcd
        message_tuple = Display.lcd_queue.get()
        text = message_tuple[0]
        row = message_tuple[1]

        # Set cursor to required row and send message
        Display.lcd.set_cursor(0, row)
        Display.lcd.message(text)

    def show_datetime24(self):
        while True:
            self.tick = not self.tick
            self._add_to_queue((dt.datetime.now().strftime(self.datetime_strings[self.tick])), 0)
            time.sleep(1)

    def loading_screen(self):
        # Loading flashtext and animation
        self.lcd.set_cursor(0, 0)
        self.lcd.message('RasPiSense')
        self.lcd.set_cursor(0, 1)
        for letter in '.........LOADING':
            self.lcd.message(letter)
            time.sleep(0.02)

        self.lcd.set_cursor(0, 1)
        for letter in '.........LOADING':
            self.lcd.message(' ')
            time.sleep(0.01)