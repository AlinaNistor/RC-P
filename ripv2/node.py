import socket
from pack import RipPack
from route_entry import RouteEntry
from header import Header


class Node:

    IP = socket.gethostbyname('0.0.0.0')
    PORT = 520
    BASE_TIMER = 5
    MAX_METRIC = 16
    ROUTE_TIMEOUT = BASE_TIMER * 6
    DELETE_TIMEOUT = BASE_TIMER * 4

    def __init__(self):
        self.neighbors = []
        self.routingTable = {}  # ipAddr : routeEntry

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update_routing_table(self):
        pass
