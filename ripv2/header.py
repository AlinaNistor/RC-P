import struct

'''

    <---------------------------32 BITS----------------------------->
    |       8       |       8       |       8       |       8       |
    =================================================================
    |    COMMAND    |    VERSION    |   UNUSED (set to all zeros)   |
    -----------------------------------------------------------------

    COMMAND - "1" for request messages and "2" for respose messages
    VERSION - vrsion of RIP protocol ( 1 or 2 )

'''


class Header:

    FORMAT = "!BBH"
    SIZE = struct.calcsize(FORMAT)
    NR_BITS_UNUSED = 16

    def __init__(self):
        self.command = 1
        self.version = 2
        self.unused = 0

    def set_header(self, header):
        _header = struct.unpack(self.FORMAT, header)
        self.command = _header[0]
        self.version = _header[1]
        self.unused = _header[2]

    def set_command(self, command):
        self.command = command

    def pack(self):
        return struct.pack(self.FORMAT, self.command, self.version, self.unused)

    def validate_header(self):
        if self.command not in [1, 2]:
            print("Invalid header")
            print("Command must be 1 or 2")
            return False

        if self.unused != 0:
            print("Invalid header")
            return False

        return True

    def __repr__(self):
        return f"{self.command} \t {self.version}"

    def __str__(self):
        return self.__repr__()
