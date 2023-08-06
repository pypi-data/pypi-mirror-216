import serial
import os


class SerialDeviceHandler(object):
    def __init__(self, port="COM1", baudrate="9600", timeout=0.2) -> None:

        self.serial_interface = serial.Serial()
        self.serial_interface.port = port
        self.serial_interface.baudrate = baudrate
        self.serial_interface.timeout = max(timeout, 0.2)

        self.buffer = str()
        self.is_open = bool()
        self.is_executing = bool()
        self.eol_delimiter = str("\n")

        self.total_rx = int(0)
        self.total_tx = int(0)

    
    def __open__(self) -> int:
        """ open port """

        if not self.is_open:
            self.serial_interface.open()
            self.is_open = True
            return 1
        return 0
    

    def __close__(self) -> int:
        """ close port """

        if self.is_open:
            self.serial_interface.close()
            self.is_open = False
            return 1
        return 0
    

    def __execution_finished__(self) -> bool:
        """ return if execution finished """

        # check if finished
        if self.buffer.split("\r\n")[-1] != "":
            return True
        return False
    

    def __process_buffer__(self) -> str:
        """ process buffer and return it """

        # localize buffer
        buffer = self.buffer

        # clear class buffer
        self.buffer = ""

        # split buffer in lines
        lined_buffer = buffer.split("\n")

        # cut last line
        buffer = "\r\n".join(lined_buffer[:-1])

        # replace \x1bE with \n
        buffer = "\n".join(buffer.split("\x1bE"))

        return buffer
    
    
    def __readline__(self) -> bytes:
        """ read lines """

        linebuffer = bytes()

        # loop until the buffer is splittable by the eol delimiter
        while len(linebuffer.decode("unicode-escape", errors="replace").split(self.eol_delimiter)) == 1:

            # read
            byte_in = self.serial_interface.read()

            # break on timeout
            if byte_in == b"":
                break

            # add to linebuffer
            linebuffer += byte_in
            self.total_rx += len(byte_in)

        return linebuffer
    

    def __read__(self, live_out: bool) -> str:
        """ get serial response, process and return it """

        last_chance = False

        # repeat reading until it finishes correctly
        while self.is_executing:

            # read line
            line_in = self.__readline__()

            # timeout
            if line_in == b"":
                if not last_chance:
                    last_chance = True
                    self.serial_interface.write("\n".encode())
                else:
                    return

            # no timeout
            else:
                last_chance = False

                # decode line and append to buffer
                self.buffer += line_in.decode("unicode-escape")

                # check for finished execution
                if self.__execution_finished__():
                    # set executing state
                    self.is_executing = False

                    # process buffer
                    buffer = self.__process_buffer__()
                    return buffer

                # print out
                if live_out:
                    print(line_in.decode("unicode-escape"), end="")
    

    def execute(self, command: str, live_out=False, write_only=False, read_only=False) -> str:
        """ executes the given command and returns the serial response """

        output = None

        # open port
        self.__open__()

        # set executing state
        self.is_executing = True

        # repeat the same command until it finishes correctly. Prevents the command from getting lost, when there is no available device
        while self.is_executing:

            # write command
            if not read_only:
                for char in command:
                    self.serial_interface.write(str(char).encode())
                    self.total_tx += len(char)
                    if write_only:
                        self.is_executing = False

            # execute
            self.serial_interface.write("\n".encode())
            self.total_tx += 1

            # start reading
            if not write_only:
                output = self.__read__(live_out)
        
        # close port
        self.__close__()
        return output