

from time import sleep
import serial
from serial.serialutil import SerialException
from pprint import pprint

class OBDII:
  # Class variables.
  _delay = 0.4
  _commands = {
    'RPM' : b'010C\n\r',
    'SPEED' : b'010D\n\r',
    'WATER' : b'0105\n\r'
  }
  _data_index = {
    'RPM' : [2,3],
    'SPEED' : 2,
    'WATER' : 2
  }

  def __init__(self, port):

    # OBD setup
    self.__connect(port)

    # Success is assumed here.
    self.__setup()
    # After here, we can communicate with the obd.

  def __setup(self):
    '''Preparing bluetooth adapter for 
    communication by OBDII-commands.
    '''
    setup_commands = [
      b'atz\n\r',     # Initiation of adapter.
      b'atl1\n\r',   
      b'ath0\n\r',
      b'atsp0\n\r'
    ]
    for command in setup_commands:
      self.ser.write(command)
      # Wait small ammount of time to make sure message
      # is recieved.
      sleep(self._delay)
    # Empty incoming buffer.
    self.ser.readlines()
    
  def __connect(self, port):
    '''Method that connects to the bluetooth
    serial port [port].
    '''
    baudrates = [38400, 9600]
    
    # Try to connect to the serial-adapter.
    for b_rate in baudrates:
      try:
        self.ser = serial.Serial(baudrate = b_rate,
          port = port, timeout = 1)
        success = True
        break
      except Exception as e:
        success = False
        print(e)
    if not success:
      raise SerialException('No baudrate resulted in connection.')


  def get_value(self, command):
    '''Request value from the car'''
    self.ser.write(self._commands[command])
    return self._parse_response(command)

  def _parse_response(self, command):
    '''Extracts data from the recieved message.'''

    response = self.ser.readlines()
    if 'SEARCHING...' in response[-1].decode():
        sleep(2)
        response = self.ser.readlines()
    print(response)
    data = response[-1].split()
    data = [byte.decode() for byte in data]
    data_index = self._data_index[command]
    # Separate idicies for every command, or at least it appears
    # to be so.
    if type(data_index) is list:
      return float(int('0x' + data[min(data_index)]
        + data[max(data_index)]), 0)
    else:
      return float(int('0x' + data[data_index], 0))

  def end(self):
    # Close the connection
    self.ser.close()

if __name__ == '__main__':
  obd = OBDII('/dev/rfcomm10')
  while True:
    pprint(obd.get_value('SPEED')) 