import socket
from pack import RipPack
from route_entry import RouteEntry
from header import Header
import ipaddress


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
        self.sock.bind((self.IP, self.PORT))

    def update_routing_table(self):
        for ipAddr, entry in self.routingTable:
            entry.update()
        self.print_routing_table()

    def print_routing_table(self):
        line = "-----------------------------------------------------------------------------"
        print(line)
        print("|      Routing Table   (Router " +
              str(socket.gethostbyname(socket.gethostname())) + ")      |")
        print(line)
        print("|Router IP  |  Metric  |  NextHop  |  Flag  |  Garbage |  Timeout |")
        print(line)
        for entry in self.routingTable:
            print(self.routingTable[entry])
            print(line)
        print("--------------------------------------------------------------------------------")
        print('\n')

    def add_route_entry(self, ipAddres, routeEntry):
        self.routingTable[ipAddres] = routeEntry
