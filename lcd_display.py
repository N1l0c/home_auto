import Adafruit_CharLCD as LCD

import SensorMeasure as poll

# General structure
while True:
    # Get measurement data
    try:
        measurement = poll.readall()

    # If wifi goes down notify on screen
    except IOError:
        # Message on screen
        pass