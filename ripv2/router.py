import sys
import os
sys.path.append(os.path.dirname('./ripv2/'))
import socket
import ipaddress
import netifaces as ni
import time
import struct
import ipcalc
import threading
from header import Header
from pack import RipPack
from route_entry import RouteEntry


class Router:

    PORT = 520
    MULTICAST_ADDRESS = '224.0.0.9'
    UPDATE_TIME = 30

    def __init__(self):
        self.routing_table = {}  # ip_addr : route_entry
        self.interfaces = self.get_interfaces()
        self.input_socket = None
        self.output_sockets = []
        self.init_input_socket()
        self.init_output_sockets()
        self.init_routing_table()

        self.update_pack = None
        self.update_trigger_flag = False

    def init_routing_table(self):
        for ip, mask in self.interfaces:
            net_address = self.get_network(ip, mask)
            entry = RouteEntry([socket.AF_INET, 1, ipaddress.IPv4Address(
                net_address), ipaddress.IPv4Address(mask), ipaddress.IPv4Address(ip), 1])
            self.routing_table[net_address] = entry

    def init_input_socket(self):  # socket for multicast receiving
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.input_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        group = socket.inet_aton(self.MULTICAST_ADDRESS)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.input_socket.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.input_socket.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        self.input_socket.bind((self.MULTICAST_ADDRESS, self.PORT))

    def init_output_sockets(self):  # sockets for sending packets to all interfaces
        for addr, _ in self.interfaces:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((addr, self.PORT))
            self.output_sockets.append(sock)

    def send_routing_table(self):
        for sock in self.output_sockets:
            print(f'send message to {sock.getsockname()}')
            sock.sendto(self.pack_routing_table(),
                        (self.MULTICAST_ADDRESS, self.PORT))

    def send_pack(self, pack):
        for sock in self.output_sockets:
            sock.sendto(pack.pack(),
                        (self.MULTICAST_ADDRESS, self.PORT))

    def receive_pack(self):
        self.input_socket.settimeout(1)
        try:
            print("receiving data...")
            data, addr = self.input_socket.recvfrom(9024)
            if addr[0] not in [addr for addr, _ in self.interfaces]:
                pack = RipPack()
                pack.unpack(data)
                self.process_received_pack(pack, addr[0])


        except Exception as e:
            print(str(e))

    def pack_routing_table(self):
        header = Header([Header.RESPONSE_MESSAGE, 2])
        rip_pack = RipPack()
        rip_pack.set_header(header)

        for ip in self.routing_table:
            rip_pack.add_entry(self.routing_table[ip])

        return rip_pack.pack()

    def process_received_pack(self, pack, addr):
        for entry in pack.route_entries:

            if not self.addr_in_routing_table(str(ipaddress.IPv4Address(entry.ip_address))) and entry.metric != 16:
                e = entry
                e.metric = e.metric + 1
                e.next_hop = ipaddress.IPv4Address(self.get_hop_address(addr))
                self.routing_table[str( ipaddress.IPv4Address(entry.ip_address))] = e

            else:
                if entry.metric == 16:

                    if self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].metric != 16:
                        self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].expired()
                        self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].next_hop = ipaddress.IPv4Address('0.0.0.0')


                elif entry.metric < self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].metric:

                    if self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].metric != 16:
                        self.routing_table[str(ipaddress.IPv4Address(
                            entry.ip_address))].metric = entry.metric
                        self.routing_table[str(ipaddress.IPv4Address(
                            entry.ip_address))].next_hop = ipaddress.IPv4Address(self.get_hop_address(addr))
                        self.routing_table[str(ipaddress.IPv4Address(
                            entry.ip_address))].reset_timeout()


                elif self.get_network(str(ipaddress.IPv4Address(entry.next_hop)), str(ipaddress.IPv4Address(entry.subnet_mask))) == self.get_network(str(self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].next_hop), str(self.routing_table[str(ipaddress.IPv4Address(entry.ip_address))].subnet_mask)):

                    self.routing_table[str(ipaddress.IPv4Address(
                        entry.ip_address))].reset_timeout()


    def get_interfaces(self):
        addresses = []
        interfaces = ni.interfaces()
        for interface in interfaces:
            try:
                ip = ni.ifaddresses(f'{interface}')[ni.AF_INET][0]['addr']
                mask = ni.ifaddresses(f'{interface}')[ni.AF_INET][0]['netmask']
                if ip.startswith('192'):
                    addresses.append([ip, mask])
            except:
                pass
        return addresses

    def addr_in_routing_table(self, addr):
        return addr in self.routing_table

    def get_hop_address(self, addr):
        network_address = self.get_network(addr, '255.255.255.0')
        for i_addr, mask in self.interfaces:
            if network_address == self.get_network(i_addr, mask):

                return i_addr

    def get_network(self, ip, mask):
        addr = ipcalc.IP(ip, mask=mask)
        network_with_cidr = str(addr.guess_network())
        network = network_with_cidr.split('/')[0]

        return network

    def print_routing_table(self):
        string = "=========================================================================\n"
        string += "|   AFI   |   Tag   |        Address       |           Mask           |      Next hop        |  Metric |  Expired flag  |   Timeout   |  Garbage   |"
        string += "=========================================================================\n"
        for ip in self.routing_table:
            string += str(self.routing_table[ip])
            string += "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        return string

    def update_route_entry(self, entry, address, new_metric, next_hop):
        if new_metric >= RouteEntry.INFINITY:
            entry.metric = RouteEntry.INFINITY
            entry.expired()
        else:
            entry.metric = new_metric

        entry.address = address
        entry.next_hop = next_hop

        if not entry.expired_flag:
            entry.reset_timeout()

    def update_timers(self):

        # trebuie schimbat cu o constanta
        header = Header([Header.RESPONSE_MESSAGE, 2])
        rip_pack = RipPack()
        rip_pack.set_header(header)

        for id in list(self.routing_table):

            # Check if the route has already expired
            if self.routing_table[id].expired_flag:
                if self.routing_table[id].garbage_remaining() <= 0:
                    self.routing_table.pop(id)
            else:
                # Check if neighbour has timed out
                if self.routing_table[id].timeout_remaining() <= 0:
                    self.routing_table[id].expired()
                    self.routing_table[id].next_hop = ipaddress.IPv4Address('0.0.0.0')
                    rip_pack.add_entry(self.routing_table[id])

        if len(rip_pack.route_entries) > 0:
            print("Sending Update")
            self.send_pack(rip_pack)

    def reset_entry_timeout(self, entry):
        entry.reset_timeout()
