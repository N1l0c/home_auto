import time
import datetime as dt
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

    def __init__(self):
        """ Constructor
        :return: Object that controls LCD display
        """

        self.tick = False    # Tick counter for clock

    #################################################################
    ''' The first few functions are just passthroughs from Adafruit_LCD
        It is possible to access any method in Adafruit_LCD using Display.lcd().method()
    '''

    @staticmethod
    def is_pressed(button):
        return Display.lcd.is_pressed(button)

    @staticmethod
    def clear():
        Display.lcd.clear()

    @staticmethod
    def set_cursor(col, row):
        Display.lcd.set_cursor(col, row)

    @staticmethod
    def message(text):
        Display.lcd.message(text)

    ################################################################
    @staticmethod
    def message_row(text, row=1, position='left'):
        """
        :param row: Display row for LCD message
        :param text String to be displayed
        :param position Display position; 'left', 'right' or 'centre'/'center'. Default 'left'
        :return: Convenience method that clears and displays method on given row, defaults to bottom row

        Strings longer than 16 char are truncated as per default behaviour
        Would be nice to integrate autoscroller later
        """
        # Set display row
        # Set to 0 if invalid argument entered
        if row == 0:
            display_row = 0
        else:
            display_row = 1

        # Set display_position
        if str(position) == 'right':
            display_position = 'right'
        elif str(position) == 'centre' or 'center':
            display_position = 'centre'
        else:
            display_position = 'left'

        # Process string for display
        # Make whitespace string
        if len(text) < 15:
            spaces = 15 - len(text)
            white_space = ' ' * spaces
        else:
            white_space = ''

        # Make message string dependent on position
        if display_position == 'left':
            message_string = text + white_space
        elif display_position == 'right':
            message_string = white_space + text
        elif display_position == 'centre':
            message_string = text

        # Set cursor at start of row
        Display.lcd.set_cursor(0, display_row)
        Display.lcd.message(message_string)


    @staticmethod
    def backlight_switch():
        Display.lcd.set_backlight(not Display.backlight_status)
        Display.backlight_status = not Display.backlight_status

    @staticmethod
    def display_readings(temp, humi):
        """
        This function displays the sensor readings
        formatted nicely on 1 x 16 character line
        """
        Display.set_cursor(0, 1)
        Display.message(('TMP:{:.1f}' + Display.degrees + ' RH:{}%').format(temp, humi))

    def display_change(self, temp_change, humi_change):
        if temp_change > 0:
            temp_arrows = self.arrows_up
        elif temp_change < 0:
            temp_arrows = self.arrows_down
        else:
            temp_arrows = '---'

        if humi_change > 0:
            humi_arrows = self.arrows_up
        elif humi_change < 0:
            humi_arrows = self.arrows_down
        else:
            humi_arrows = '---'

        self.lcd.set_cursor(0, 1)
        self.lcd.message('TMP:{}   RH:{}'.format(temp_arrows, humi_arrows))

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

    def show_time24(self, position='top right'):
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
            col = 10
        while True:
            self.tick = not self.tick
            self.lcd.set_cursor(col, row)
            self.lcd.message(dt.datetime.now().strftime(self.time_strings[self.tick]))
            time.sleep(1)

    def show_datetime24(self, row=0):
        # Set display row
        # Set to 0 if invalid argument entered
        if row != 0 or row != 1:
            display_row = 0
        else:
            display_row = row

        while True:
            self.tick = not self.tick
            self.lcd.set_cursor(0, display_row)
            self.lcd.message(dt.datetime.now().strftime(self.datetime_strings[self.tick]))
            time.sleep(1)
