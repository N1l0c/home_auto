# Imports
import urllib
import datetime as dt
import time
from string import Template
import Adafruit_CharLCD as LCD

# Initialise LCD using pins
lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(1,1,1)

backlightstatus = True

# Define LCD functions
def msgLn(msg, row):
    #global lcd
    lcd.set_cursor(0, row)
    lcd.message(msg)

def msgCl(msg):
    #global lcd
    lcd.clear()
    lcd.message(msg)

def msgInsert(msg, column, row):
    lcd.set_cursor(column, row)
    lcd.message(msg)

def msgTyped(msg, row, pause):
    lcd.set_cursor(0, row)
    for letter in msg:
        lcd.message(letter)
        time.sleep(pause)

def switchBL():
    if backlightstatus == True:
        lcd.set_color(*on)
    elif backlightstatus == False:
        lcd.set_color(*off)

def switchBLpress():
    global backlightstatus
    # Check for backlight change
    if lcd.is_pressed(LCD.SELECT):
        backlightstatus = not backlightstatus
        switchBL()

# This flashes the display on and off a certain color
def flashCol(color, times):
    for i in range(times):
        lcd.set_color(*color)
        time.sleep(0.05)
        lcd.set_color(*on)
        time.sleep(0.05)

# Data/string functions
def sbtrct(now, prev):
    return float(now) - float(prev)

def diff(now, prev):
    return map(sbtrct, now, prev)

def addChar(msg, char):
    msg = msg + char
    return msg

def arrow(delta, val):
    global backlightstatus
    if delta == 0:
        return val
    if delta > 0:
        if backlightstatus == True:
            flashCol(red, 3)
        return up
    elif delta < 0:
        if backlightstatus == 1:
            flashCol(blue, 3)
        return down

# Colours & custom characters
lcd.create_char(0, [24, 24, 3, 4, 4, 4, 3, 0])  # Create a degrees character
lcd.create_char(1, [4,14,21,4,4,0,0,0])  # Up arrow
lcd.create_char(2, [0,0,4,4,21,14,4,0])  # Down arrow

lcd.create_char(3, [16,16,16,16,16,16,16,16])  # 20pc box
lcd.create_char(4, [28,28,28,28,28,28,28,28])  # 60pc box
lcd.create_char(5, [31,31,31,31,31,31,31,31])  # 100pc box

#lcd.create_char(6, [0,14,17,21,17,14,0,0])      # Loading circle 2
#lcd.create_char(7, [0,14,31,31,31,14,0,0])      # Loading circle 1

boxfills = ['\x03', '\x04', '\x05']


deg = '\x00'
up = '\x01\x01\x01  '
down = '\x02\x02\x02  '

red = (1, 0, 0)
blue = (0, 0, 1)
off = (0, 0, 0)
on = (1, 1, 1)

##############################
# Create a read function
# NB this includes backlight checking because its so slow
# Threading with a watched queue may be a good solution to that
def readAll():

    # Poll server for page srcs
    msgInsert(' ', 13, 1)
    sockT = urllib.urlopen("http://192.168.1.57/temp")
    srcT = sockT.read()
    switchBLpress()

    msgInsert(':', 13, 1)
    sockH= urllib.urlopen("http://192.168.1.57/humidity")
    srcH = sockH.read()
    switchBLpress()

    Temperature = srcT.split(" ",1)
    Humidity = srcH.split(" ",1)

    Temp = Temperature[1].strip(' F')
    Hum = int(Humidity[1].strip('%'))

    TempC = (float(Temp) -32) / 1.8

    sockT.close()
    sockH.close()

    return (TempC, Hum)
##############################

######################################################################

# Show welcome messages on the LCD
msgCl('TEMP/HUM DISPLAY')
msgLn('\nby Colin Freeth', 0)
time.sleep(0.5)

# Make a starting graphic
loadMessage = 'STARTING UP.....'
msgTyped(loadMessage, 0, 0.07)

# Make Loading bar animation
for char in range(16):
    for slice in boxfills:
        lcd.set_cursor(char, 1) # Set cursor position
        lcd.message(slice)
        time.sleep(0.02)

# # Special time for Magnus
# lcd.clear()
# msgTyped('HOL UP.\n', 0, 0.3)
# lcd.message('DIS. ')
# time.sleep(0.3)
# lcd.message('TIME.')
# time.sleep(0.5)
# msgCl('IT\'S ')
# time.sleep(0.5)
# lcd.message('FOR')
# time.sleep(0.5)
# msgTyped('...',1 , .8)
# msgLn('MAGNUS',1)
# time.sleep(1)
# msgCl('U ')
# time.sleep(1)
# lcd.message('LIL ')
# time.sleep(1)
# lcd.message('PUNK')
# time.sleep(1)
# msgTyped('BIIIIIIIIIIIIIII', 1, 0.3)
# lcd.clear()
# for i in range(200):
#     msgTyped('IIIIIIIIIIIIIII', i % len(range(2)), 1 / float(10 + 3.141 ** i))
#     lcd.clear()
# msgLn('IIIIIIIIIIII', 1)
# for i, letter in enumerate('TCH.'):
#     lcd.message(letter)
#     time.sleep(i + 1)
# time.sleep(3)
# lcd.clear()

# Template string for display and blank dict for strings
msgStr = Template('TMP:${temp} RH:${humi}')
msgDict = {'temp' : '---',
           'humi' : '---' }

# Initialise lastData to reasonable values for diff calculation
lastData = [0, 0]

n = 0  # Attempt counter fo IOError counting

# Show date and time first
timeStr = dt.datetime.now().strftime('%a %d %b %H:%M')
msgLn(timeStr, 1)

while True:
    # Get measurement data and store changes
    try:
        data = readAll()
        change = diff(data, lastData)
        timeStr = dt.datetime.now().strftime('%a %d %b %H:%M')

        # ONLY CHANGE LCD IF VALUES CHANGE
        if change[0] or change[1] != 0:
            # Change to character if value changed
            msgDict['temp'] = arrow(change[0], msgDict['temp'])
            msgDict['humi'] = arrow(change[1], msgDict['humi'])
            # Send formatted message to LCD
            msgLn(msgStr.substitute(msgDict), 0)
            time.sleep(0.5)

            # Add formatted data strings to msgDict
            msgDict['temp'] = '{:.1f}\x00'.format(data[0])
            msgDict['humi'] = '{}%'.format(data[1])

            # Send formatted message to LCD
            msgLn(msgStr.substitute(msgDict), 0)

        # Print time and date on bottom
        msgLn(timeStr, 1)

        lastData = data
        n = 0  #Reset attempt counter
    #   time.sleep(2)  # Wait for new reading

    except IOError:
        print('IOError')
        n += 1
        msgCl('READ FAILED')
        time.sleep(0.3)
        msgLn('\nTRYING AGAIN', 1)
        time.sleep(0.3)
        msgLn(('\nATTEMPT:%d.......' % n), 1)
