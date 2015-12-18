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

# Instantiate sensor and show blank readings
# room1 = Sensor.Sensor('Front Room', '192.168.1.57')
# lcd.message(measStr.substitute(measDict))
# lcd.message('\n' + room1.timeFormat())


# Threading to try and speed up the IO slowness of urlopen
def sensorget(dataQueue):
    room1 = Sensor.Sensor('Front Room', '192.168.1.57')
    while True:
        room1.now()
        dataQueue.put(room1)
        print room1
        print('Put something in the queue!')


def data_display(dataQueue):
    while True:
        latest = dataQueue.get()
        lcd.home()
        lcd.message(('TMP:{:.1f}' + degrees + ' RH:{}%').format(latest.temp, latest.humi))
        print('Tried to print a message!')


# Create Queue for passing data from sensor
measureQueue = Queue.LifoQueue()

sensorThread = threading.Thread(target=sensorget(measureQueue))
sensorThread.daemon = True
lcdThread = threading.Thread(target=data_display(measureQueue))
lcdThread.daemon = True
sensorThread.start()
lcdThread.start()

