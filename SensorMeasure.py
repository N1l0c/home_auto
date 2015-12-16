# Create a read function
# Threading with a watched queue may be a good solution to that
import urllib


class SensorMeasure:

    def __init__(self, location, ipaddress):
        self.temp = 21.0
        self.humi = 35
        self.loc = location
        self.ip = ipaddress

    def now(self):
        # Download page sources
        sockt = urllib.urlopen('http://' + self.ip + '/temp')
        srct = sockt.read()
        sockt.close()
        sockh = urllib.urlopen('http://' + self.ip + 'humidity')
        srch = sockh.read()
        sockh.close()

        # Split, strip strings and set values
        tempf = srct.split(' ', 1)[1].strip(' F')
        self.humi = int(srch.split(' ', 1)[1].strip('%'))
        self.temp = (float(tempf) - 32) / 1.8  # Convert temperature to celcius

    def delta(self, previousmeasure):
        deltat = previousmeasure.temp - self.temp
        deltah = previousmeasure.humi - self.humi
        return deltat, deltah