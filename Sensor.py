import urllib
import datetime as dt
import time
import threading

from w1thermsensor import W1ThermSensor


class AutoUpdating(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, loc, ip, sensor='dht'):
        """ Constructor
        :rtype: Sensor Object
        :type self.location: str
        :param self.location: Location (room) of sensor
        :type self.temp: float
        :type self.ip_address: str
        """
        self.temp = 0.0
        self.humi = 0
        self.temp_change = None
        self.humi_change = None
        self.temp_previous = 0.0
        self.humi_previous = 0
        self.has_changed = False
        self.ip_address = ip
        self.location = loc
        self.measurement_time = dt.datetime.now()
        self.sensor_type = sensor
        self.dsb_sensor = None

        # Start the relavent sensor update thread
        if self.sensor_type == 'dht':
            thread = threading.Thread(target=self._dht_updater, args=())
        elif self.sensor_type == 'dsb':
            thread = threading.Thread(target=self._dsb_updater, args=())

        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def _dht_updater(self):
        """ Method constantly gets latest DHT22 sensor readings from server """
        while True:
            self.temp_previous = self.temp
            self.humi_previous = self.humi
            self.timelast = self.measurement_time

            # Download page sources
            sockt = urllib.urlopen('http://' + self.ip_address + '/temp')
            srct = sockt.read()
            sockt.close()
            # Set new measurement time
            self.measurement_time = dt.datetime.now()
            sockh = urllib.urlopen('http://' + self.ip_address + '/humidity')
            srch = sockh.read()
            sockh.close()

            # Split, strip strings and set values
            tempf = srct.split(' ', 1)[1].strip(' F')
            self.humi = int(srch.split(' ', 1)[1].strip('%'))
            self.temp = (float(tempf) - 32) / 1.8  # Convert temperature to celcius

            # Calculate change values
            self.temp_change = self.temp - self.temp_previous
            self.humi_change = self.humi - self.humi_previous

            # Flag change
            if (self.temp_change or self.humi_change) != 0:
                self.has_changed = True
            else:
                self.has_changed = False

            time.sleep(2)

    def _dsb_updater(self):
        """
        Method for DSB sensor update
        :return: DSB sensor readings
        """
        self.dsb_sensor = W1ThermSensor()
        self.humi = '---'
        self.humi_change = 0
        while True:
            # Set previous values
            self.temp_previous = self.temp
            self.humi_previous = self.humi
            self.timelast = self.measurement_time

            self.temp = self.dsb_sensor.get_temperature()
            # Calculate change values
            self.temp_change = self.temp - self.temp_previous

            # Flag change
            if self.temp_change != 0:
                self.has_changed = True
            else:
                self.has_changed = False

            time.sleep(2)


# Test Code
if __name__ == '__main__':

    front_room = AutoUpdating('Front Room', '192.168.1.57')
    while True:
        if front_room.has_changed:
            print front_room.temp
