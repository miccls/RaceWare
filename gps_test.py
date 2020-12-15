# gps_test.py
import serial
import pynmea2

        '''Initierar GPS port vald i settings.py.'''
        GPS_port = "/dev/ttyAMA0"
        ser = serial.Serial(GPS_port, baudrate = 9600, timeout = 0.5)
        data_out = pynmea2.NMEAStreamReader()
        while True:
            new_data = ser.readline()
            while new_data[0:6] != '$GPGLL':
                new_data = ser.readline()
            new_msg = pynmea2.parse(new_data)
            lat = new_msg.latitude
            lon = new_msg.longitude
            print(f"Latitud : {lat}, Longitud: {lon}")