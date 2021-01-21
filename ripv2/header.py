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
    REQUEST_MESSAGE = 1
    RESPONSE_MESSAGE = 2

    def __init__(self, data):
        self.command = data[0]
        self.version = data[1]
        self.unused = 0

        self.validate_header()

    def set_command(self, command):
        self.command = command

    def pack(self):
        return struct.pack(self.FORMAT, self.command, self.version, self.unused)

    def validate_header(self):
        if self.command not in [1, 2]:
            raise Exception("(RIP HEADER) Command must be 1 or 2")

        if self.unused != 0:
            raise Exception("(RIP HEADER) Unused bits are not set to zeros")
        
        if self.version not in [1, 2]:
            raise Exception("(RIP HEADER) Inavlid protocol version")

    def __str__(self):
        return f"{self.command} \t {self.version}"
