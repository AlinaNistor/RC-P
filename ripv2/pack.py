import socket

class RipPack:
    def __init__(self):
        self.ip = socket.gethostbyname('0.0.0.0')
        self.header = None
        self.route_entries = []
    
    def add_entry(self, route_entry):
        self.route_entries.append(route_entry)
    
    def set_header(self, header):
        self.header = header
    