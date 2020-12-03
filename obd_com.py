import obd

class OBDII:
  def __init__(self,main, command_dict):
    # OBD setup

    obd.logger.setLevel(obd.logging.DEBUG)

    # Connect to OBDII adapter
    ports = obd.scan_serial()
    self.connection = obd.OBD(ports[0])
    # Print supported commands

    # List of commands for different information

    self.commands = connection.supported_commands
    print("Supported commands: ")
    for command in commands:
      print(command.name)
    # Loop to delete unsupported commands from main list.
    # Doing this we know which gauges to print.
    for key, value in main.command_list:
      for command in commands:
        if command.name == value:
          continue
        del main.command_list[key]

  

# Send a command
  def get_value(self, command_arg):
    command = command_arg
    if (command == "quit"):
      pass
    try:
      res = self.connection.query(obd.commands[command])
      return res.value
    except Exception as ex:
      print("Error: " + str(ex))

  def end(self):
    # Close the connection
    connection.close()
if __name__ == '__main__':
  obd2 = OBDII()
