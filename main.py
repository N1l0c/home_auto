import time
import threading

import Sensor
import LCD

##############################
# Initialise LCD display
lcd = LCD.Display()

# Sensors setup
room1 = Sensor.AutoUpdating('Front Room', '192.168.1.57')
# # Make another one to test multi room functionality
room2 = Sensor.AutoUpdating('RasPi', 'localhost', 'dsb')
# room3 = Sensor.AutoUpdating('Bathroom', '192.168.1.57')

# Create reference lists
sensors = [room1, room2]
current = 0  # Initialises room counter
# Buttons
dpad_buttons = ((lcd.left, -1),
                (lcd.right, +1),
                (lcd.up, +1),
                (lcd.down, -1))

##############################

# Display loading screen until reading retrieved from first active sensor
while not sensors[current].has_changed:
    lcd.loading_screen()

# Clear display and start datetime thread
lcd.clear()
# Start daemon thread for datetime display on first row with ticking colon
datetime24_thread = threading.Thread(target=lcd.show_datetime24, args=())
datetime24_thread.daemon = True  # Yep, it's a daemon, when main thread finish, this one will finish too
datetime24_thread.start()  # Start it!
lcd.message_row(sensors[current].location)
time.sleep(1)
lcd.display_readings(sensors[current].temp, sensors[current].humi)


try:
    while True:
        if lcd.is_pressed(lcd.select):
            print 'pressed'
            lcd.backlight_switch()
            while lcd.is_pressed(lcd.select):
                pass

        for button in dpad_buttons:
            if lcd.is_pressed(button[0]):
                # Wait for button release for niceness
                while lcd.is_pressed(button[0]):
                    pass  # Wait for button release before proceeding
                # Change displayed sensor
                current = (current + button[1]) % len(sensors)
                # On bottom row, display location for 1 sec and then readings
                lcd.message_row(sensors[current].location)
                time.sleep(1)
                lcd.display_readings(sensors[current].temp, sensors[current].humi)

        if sensors[current].has_changed:

            # Display directional arrows for a short time to show change
            lcd.set_cursor(0, 1)
            lcd.display_change(sensors[current].temp_change, sensors[current].humi_change)
            time.sleep(0.8)

            # Set cursor to bottom row each time
            lcd.set_cursor(0, 1)
            lcd.display_readings(sensors[current].temp, sensors[current].humi)
            sensors[current].has_changed = False

# Exit cleanly on the LCD
except KeyboardInterrupt:
    lcd.clear()
    lcd.lcd.set_color(1, 0, 0)
    lcd.message_row('TERMINATED')
    time.sleep(1)
    lcd.message_row('USER CTRL+C')
    time.sleep(3)
    lcd.clear()
    lcd.lcd.set_backlight(0)


