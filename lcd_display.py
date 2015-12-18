import threading
from string import Template
import Queue

import Adafruit_CharLCD as LCD
import Sensor

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


##############################
room1 = Sensor.AutoUpdating('Front Room', '192.168.1.57')

while True:
    lcd.home()
    lcd.message(('TMP:{:.1f}' + degrees + ' RH:{}%').format(room1.temp, room1.humi))
