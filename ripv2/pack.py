import struct
from header import Header
from route_entry import RouteEntry

class RipPack:
    def __init__(self):
        self.header = None
        self.route_entries = []
    
    def add_entry(self, route_entry):
        self.route_entries.append(route_entry)

    def set_header(self, header):
        self.header = header
    
    def set_entries(self, route_entries):
        self.route_entries = route_entries
    
    def pack(self):
        data = self.header.pack()
        for entry in self.route_entries:
            data += entry.pack()

        return data

    def unpack(self, encoded_data):
        self.header = Header(struct.unpack(Header.FORMAT, encoded_data[: Header.SIZE]))
        entries_data = encoded_data[Header.SIZE:]

        for i in range(0, len(entries_data), RouteEntry.SIZE):
            entry = struct.unpack(RouteEntry.FORMAT, entries_data[i: i + RouteEntry.SIZE])
            self.route_entries.append(RouteEntry(entry))

    
    def print_pack(self):
        print(self.header)
        print()
        for entry in self.route_entries:
            print(entry)
