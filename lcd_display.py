
from string import Template

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

# String templates for LCD
measStr = Template('TMP:${tempval}' + degrees + ' RH:${humival}%')
measDict = {'tempval': '---',
            'humival': '---'}

##############################

# Instantiate sensor and show blank readings
room1 = Sensor.Sensor('Front Room', '192.168.1.57')
lcd.message(measStr.substitute(measDict))
lcd.message('\n' + room1.timeFormat())

# Main loop
while True:
    try:
        room1.now()  # Get current readings
        # Format values for LCD and store in relevant dictionary entry
        measDict['tempval'] = '{:.1f}'.format(room1.temp)
        measDict['humival'] = '{}'.format(room1.humi)

        # Update display if change
        if (room1.delta()[0] or room1.delta()[1]) != 0:
            lcd.clear()
            lcd.message(measStr.substitute(measDict))
            lcd.message('\n' + room1.timeFormat())
        else:
            lcd.home()
            lcd.message('\n' + room1.timeFormat())

    # If wifi goes down notify on screen
    except IOError:
        # Message on screen
        pass
