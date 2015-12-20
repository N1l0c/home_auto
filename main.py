import time
import threading

import Sensor
import LCD

##############################
# Initialise LCD display
lcd = LCD.Display()
lcd_time = LCD.Time()

# Sensors setup
room1 = Sensor.AutoUpdating('Front Room', '192.168.1.57')
# Make another one to test multi room functionality
# room2 = Sensor.AutoUpdating('Kitchen', '192.168.1.57')
# room3 = Sensor.AutoUpdating('Bathroom', '192.168.1.57')

# Create reference lists
sensors = [room1]
current = 0  # Initialises room counter
# Buttons
buttons = ((lcd.left, -1),
           (lcd.right, +1),
           (lcd.up, +1),
           (lcd.down, -1),
           (lcd.select, +1))

##############################

# Display loading screen until reading retrieved from room1
while not room1.has_changed:
    lcd.loading_screen()

lcd.clear()
lcd.message(sensors[current].location)
lcd.display_readings(sensors[current].temp, sensors[current].humi)

# Start daemon thread for time display with ticking colon
lcd_t = threading.Thread(target=lcd_time.show_time24, args=())
lcd_t.daemon = True  # Yep, it's a daemon, when main thread finish, this one will finish too
lcd_t.start()  # Start it!

print 'Got to main thread'

while True:
    if sensors[current].has_changed:
        print 'change sensed'
        print sensors[current].measurement_time
        print sensors[current].temp
        print sensors[current].humi

        lcd.set_cursor(0, 1)
        lcd.display_change(sensors[current].temp_change, sensors[current].humi_change)
        time.sleep(0.5)

        # Set cursor to bottom row each time
        lcd.set_cursor(0, 1)
        lcd.display_readings(sensors[current].temp, sensors[current].humi)
        sensors[current].has_changed = False


#####################################
# This section contains temporary/previous code to be reimplemented

#     for button in buttons:
#         if lcd.is_pressed(button[0]):
#             # Wait for button release for niceness
#             while lcd.is_pressed(button[0]):
#                 pass  # Wait for button release before proceeding
#             # Change displayed sensor
#             current = (current + button[1]) % len(sensors)
#             # On bottom row, display location for 1 sec and then readings
#             lcd.set_cursor(0, 1)
#             lcd.message(sensors[current].location)
#             time.sleep(1)
#             lcd.display_readings(sensors[current].temp, sensors[current].humi)
