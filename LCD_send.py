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

        sender = threading.Thread(target=self._send_message, args=())
        sender.daemon = True
        sender.start()

    #################################################################
    @staticmethod
    def _add_to_queue(text, row=1):
        """

        :param message_tuple: Tuple containing message string, row
        :return:
        """
        Display.lcd_queue.put((text, row))

    @staticmethod
    def _send_message():
        # Runs forever
        while True:
            # Get message parameters from Queue and send message to lcd
            message_tuple = Display.lcd_queue.get()
            text = message_tuple[0]
            row = message_tuple[1]

            # Set cursor to required row and send message
            Display.lcd.set_cursor(0, row)
            Display.lcd.message(text)

    def message(self, text, row=1):
        """
        This method takes input text string and adds whitespace if necessary. It then sends to _add_to_queue.
        :param text: Text string to be sent to LCD
        :param row: Row to be displayed on
        :return:
        """
        # Set display row
        # Set to 0 if invalid argument entered
        if row == 0:
            display_row = 0
        else:
            display_row = 1

        # Process string for display
        # Make whitespace string
        if len(text) < 15:
            spaces = 16 - len(text)
            white_space = ' ' * spaces
        else:
            white_space = ''

        # Add whitespace to message and then add to message queue
        message_string = text + white_space
        self._add_to_queue(message_string, display_row)

    def show_datetime24(self):
        """
        Infinite loop to display date and time with flashing colon on top row, called as background thread in main
        :return:
        """
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