from events import Events
from flash_lamp import FlashLamp
from gazepoint_parser import *
import numpy as np
from processor import *
import serial
import socket
from threading import Thread
import time


class GazePoint(object):

    def __init__(self):
        # Define Gazepoint host/port...
        self.host = '127.0.0.1'
        self.port = 4242
        self.address = (self.host, self.port)
        self.connected = False
        self.lamp = FlashLamp()
        self.go = True
        self.is_collecting = False
        self.events = Events()

        # Establish connection to Gazepoint.
        try:
            print('Establishing connection to Gazepoint.')
            self.socket = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.address)
            s.send(str.encode('<SET ID="ENABLE_SEND_TIME" STATE="1" />\r\n'))
            s.send(str.encode('<SET ID="ENABLE_SEND_EYE_LEFT" STATE="1" />\r\n'))
            s.send(str.encode('<SET ID="ENABLE_SEND_EYE_RIGHT" STATE="1" />\r\n'))
            s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))
            self.connected = True
        except:
            print('Cannot establish connection to Gazepoint.')
            self.connected = False

    def collect(self, scan):
        # Start collecting from the Gazepoint system.
        self.scan = scan

        # Start collecting data.
        scanner_data = []
        python_time = []
        start_time = time.time()
        min_time = np.inf
        max_time = 0
        flashed = False
        flash_time = 0

        # Standard 16 second scan.
        while (time.time() - start_time) < 16:

            # Grab the time stamp.
            rx_data = self.socket.recv(512)
            xml_obs = bytes.decode(rx_data)
            ts = xml_to_time(xml_obs)
            python_time.append(time.time())

            # Append raw XML observations
            scanner_data.append(xml_obs)

            # Should we flash the lamp?
            if (time.time() - start_time) >= 8:
                if not flashed:
                    print('Flashing Lamp')
                    flash_time = (time.time(), ts)
                    self.lamp.flash_lamp()
                    flashed=True

        # We are done. Now parse the data, etc.
        print('Finished Data Collection')
        return flash_time, scanner_data
    
        obs = parse_data(scanner_data)
        data = generate_time_series(obs)
        return data
        self.scan = j6_analysis(data, self.scan)
        try:
            self.scan['isSuccess'] = True
        except:
            self.scan['isSuccess'] = False

        # Announce we are finished!
        print('Processing Complete')
        return self.scan



    def kill(self):
        self.socket.close()
        self.lamp.kill()
