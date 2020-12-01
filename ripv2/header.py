import struct


class Header:
    '''

    <---------------------------32 BITS----------------------------->
    |       8       |       8       |       8       |       8       |
    =================================================================
    |    COMMAND    |    VERSION    |   UNUSED (set to all zeros)   |
    -----------------------------------------------------------------

    COMMAND - "1" for request messages and "2" for respose messages
    VERSION - vrsion of RIP protocol ( 1 or 2 )

    '''
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
