import urllib
import datetime as dt
import threading


class AutoUpdating(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, loc, ip):
        """ Constructor
        :type loc: str
        :param self.location: Location (room) of sensor
        """
        self.temp = 0.0
        self.humi = 0
        self.temp_previous = 0.0
        self.humi_previous = 0
        self.has_changed = False
        self.ipaddress = ip
        self.location = loc
        self.time = dt.datetime.now()

        thread = threading.Thread(target=self.updater, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def updater(self):
        """ Method that runs forever """
        while True:
            self.temp_previous = self.temp
            self.humi_previous = self.humi
            self.timelast = self.time

            # Download page sources
            sockt = urllib.urlopen('http://' + self.ipaddress + '/temp')
            srct = sockt.read()
            sockt.close()
            self.time = dt.datetime.now()  # Set new measurement time
            sockh = urllib.urlopen('http://' + self.ipaddress + '/humidity')
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


# Test Code
if __name__ == '__main__':

    front_room = AutoUpdating('Front Room', '192.168.1.57')
    while True:
        if front_room.has_changed:
            print front_room.temp
