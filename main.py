import time

import Sensor
import LCD

##############################
# Initialise LCD display
lcd = LCD.Display()

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
lcd.display_readings(sensors[current].temp, sensors[current].humi)

while True:
    for button in buttons:
        if lcd.is_pressed(button[0]):
            # Wait for button release for niceness
            while lcd.is_pressed(button[0]):
                pass  # Wait for button release before proceeding
            # Change displayed sensor
            current = (current + button[1]) % len(sensors)
            # On bottom row, display location for 1 sec and then readings
            lcd.set_cursor(0, 1)
            lcd.message(sensors[current].location)
            time.sleep(1)
            lcd.display_readings(sensors[current].temp, sensors[current].humi)

    if sensors[current].has_changed:
        print 'change sensed'

        lcd.set_cursor(0, 1)
        lcd.display_change(sensors[current].temp_change, sensors[current].humi_change)
        time.sleep(0.5)

        # Set cursor to bottom row each time
        lcd.set_cursor(0, 1)
        lcd.display_readings(sensors[current].temp, sensors[current].humi)
        sensors[current].has_changed = False
