

from time import sleep
import serial
from serial.serialutil import SerialException
from pprint import pprint

class OBDII:
  # Class variables.
  _delay = 0.4
  _commands = {
    'rpm' : b'010C\r',
    'kmh' : b'010D\r',
    'water' : b'0105\r'
  }
  _data_index = {
    'rpm' : -2,
    'kmh' : -1,
    'water' : -1
  }

  def __init__(self, port):

    # OBD setup
    self.port = port
    self.__connect()

    # Success is assumed here.
    self.__setup()
    # After here, we can communicate with the obd.

  def __setup(self):
    '''Preparing bluetooth adapter for 
    communication by OBDII-commands.
    '''
    setup_commands = [
      b'atz\r',     # Initiation of adapter.
      b'atl1\r',   
      b'ath0\r',
      b'atat2',
      b'atsp0\r'
    ]
    for command in setup_commands:
      self.ser.write(command)
      # Wait small ammount of time to make sure message
      # is recieved.
      sleep(self._delay)
    # Empty incoming buffer.
    self.ser.readlines()
    
  def __connect(self,):
    '''Method that connects to the bluetooth
    serial port [port].
    '''
    b_rate = 38400
    e = ""
    # Try to connect to the serial-adapter.
    try:
      self.ser = serial.Serial(baudrate = b_rate,
        port = self.port, timeout = 1)
      success = True
      return
    except Exception as e:
      message = e
    if "[Errno 2]" in e:
      # If the prechosen port can't be opened.
      success = self._handle_port_error()
    if not success:
      raise SerialException('No baudrate resulted in connection.')

  def _handle_port_error(self) -> bool:
    '''Handle situation where port can't be
    opened. 
    '''
    # Try port 0 -> 99
    for i in range(100):
      try:
        self.ser = serial.Serial(baudrate = 38400,
          port = "/dev/rfcomm" + str(i), timeout = 1)
        return True
      except Exception:
        pass
    # Could not connect.
    return False

  def get_value(self, command):
    '''Request value from the car'''
    self.ser.write(self._commands[command])
    return self._parse_response(command)

  def _parse_response(self, command):
    '''Extracts data from the recieved message.'''
    response = self.ser.readlines()
    # If it goes though connection process, wait.
    if 'SEARCHING...' in response[-1].decode():
        sleep(5)
        response = self.ser.readlines()
    #print(response)
    # Dictionary with keys representing number of "words".
    data = {len(line.split()): line.split() for line in response}
    data = data[max(list(data.keys()))]
    data = [byte.decode() for byte in data]
    data_index = self._data_index[command]
    # Separate idicies for every command, or at least it appears
    # to be so.
    try:
          return float(int('0x' + \
            self.unpackData(data[data_index:]), 0))

    except (ValueError, KeyError) as e:
        print(data, e, sep = '\n')
        # To avoid a NoneType error.
        return 0

  @classmethod
  def unpackData(cls, arr):
    '''Recursive metod that unpacks array 
    of strings.
    '''
    # Will evaluate to False if empty.
    if arr:
      return arr[0] + cls.unpack(arr[1:])
    else:
      return ''

  def end(self):
    # Close the connection
    self.ser.close()

if __name__ == '__main__':
  obd = OBDII('/dev/rfcomm10')
  while True:
    print(obd.get_value('kmh')) 