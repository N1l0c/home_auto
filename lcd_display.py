import time
import threading
from string import Template
import Queue

import Adafruit_CharLCD as LCD
import Sensor
import lcd_time

##############################

# LCD setup and functions
lcd = LCD.Adafruit_CharLCDPlate()

# Custom characters
lcd.create_char(0, [24, 24, 3, 4, 4, 4, 3, 0])  # Create a degrees character
lcd.create_char(1, [4, 14, 21, 4, 4, 0, 0, 0])  # Up arrow
lcd.create_char(2, [0, 0, 4, 4, 21, 14, 4, 0])  # Down arrow
degrees = '\x00'
up = '\x01\x01\x01'
down = '\x02\x02\x02'


def display_reading(sensor):
    """
    This function displays the sensor readings
    formatted nicely on 1 x 16 character line
    """
    lcd.set_cursor(0, 1)
    lcd.message(('TMP:{:.1f}' + degrees + ' RH:{}%').format(sensor.temp, sensor.humi))


##############################
# Initialise AutoUpdating Sensor object
room1 = Sensor.AutoUpdating('Front Room', '192.168.1.57')
# Make another one to test multi room functionality
room2 = Sensor.AutoUpdating('Kitchen', '192.168.1.57')
room3 = Sensor.AutoUpdating('Bathroom', '192.168.1.57')

# Create reference list
sensors = [room1, room2, room3]
current = 0  # Initialises room counter

# Loading flashtext and animation
lcd.clear()
lcd.message('RasPiSense\nby Colin Freeth')
time.sleep(0.5)
lcd.clear()
lcd.message('RasPiSense')
while room1.temp == 0.0:
    lcd.set_cursor(0, 1)
    for letter in '.........LOADING':
        lcd.message(letter)
        time.sleep(0.02)

    lcd.set_cursor(0, 1)
    for letter in '.........LOADING':
        lcd.message(' ')
        time.sleep(0.02)

lcd.clear()
lcd.message(sensors[current].location)
display_reading(sensors[current])

while True:
    if lcd.is_pressed(LCD.RIGHT):
        while lcd.is_pressed(LCD.RIGHT):
            pass  # Wait for button release before proceeding
        current = (current + 1) % len(sensors)
        lcd.clear()
        lcd.message(sensors[current].location)
        display_reading(sensors[current])

    if lcd.is_pressed(LCD.LEFT):
        while lcd.is_pressed(LCD.LEFT):
            pass  # Wait for button release before proceeding
        current = (current - 1) % len(sensors)
        lcd.clear()
        lcd.message(sensors[current].location)
        display_reading(sensors[current])

    if sensors[current].has_changed:
        print 'change sensed'
        # Set cursor to bottom row each time
        lcd.set_cursor(0, 1)
        display_reading(sensors[current])
        sensors[current].has_changed = False
