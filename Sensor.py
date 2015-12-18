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
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.temp = 0.0
        self.humi = 0
        self.ipaddress = ip
        self.location = loc
        self.time = dt.datetime.now()
        thread = threading.Thread(target=self.updater, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def updater(self):
        """ Method that runs forever """
        while True:
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


# The sensor class contains current and previous measurements,
# the measurement time as a datetime object
# as well as location and ip address strings
# class Sensor(object):
#     def __init__(self, location, ipaddress):
#         self.time = dt.datetime.now()
#         self.temp = 0.0
#         self.humi = 0
#         self.loc = location
#         self.ip = ipaddress
#
#     def now(self):
#         # Set last measurement values
#         self.templast = self.temp
#         self.humilast = self.humi
#         self.timelast = self.time
#         # Download page sources
#         sockt = urllib.urlopen('http://' + self.ip + '/temp')
#         srct = sockt.read()
#         sockt.close()
#         self.time = dt.datetime.now()  # Set new measurement time
#         sockh = urllib.urlopen('http://' + self.ip + '/humidity')
#         srch = sockh.read()
#         sockh.close()
#         # Split, strip strings and set values
#         tempf = srct.split(' ', 1)[1].strip(' F')
#         self.humi = int(srch.split(' ', 1)[1].strip('%'))
#         self.temp = (float(tempf) - 32) / 1.8  # Convert temperature to celcius
#
#     # The delta function returns the difference between the last measurement
#     # and the current measurement as a tuple
#     @property
#     def delta(self):
#         tempdelta = self.templast - self.temp
#         humidelta = self.humilast - self.humilast
#         return tempdelta, humidelta
#
#     # Returns a nicely datetime string
#     def timeFormat(self, layout='%a %d %b %H:%M'):
#         return self.time.strftime(layout)
