import struct
import ipaddress
import time
'''
    <---------------------------32 BITS----------------------------->
    |       8       |       8       |       8       |       8       |
    =================================================================
    |   ADDRESS FAMILY IDENTIFIER   |            ROUTE TAG          |
    -----------------------------------------------------------------
    |                           IP ADDRESS                          |
    -----------------------------------------------------------------
    |                           SUBNET MASK                         | 
    -----------------------------------------------------------------
    |                             NEXT HOP                          |
    -----------------------------------------------------------------
    |                             METRIC                            |
    -----------------------------------------------------------------  

    METRIC - The metric field contains a value between 1 and 15 (inclusive) which
            specifies the current metric for the destination; or the value 16
            (infinity), which indicates that the destination is not reachable
'''

class RouteEntry:

    FORMAT = "!HHIIII"
    SIZE = struct.calcsize(FORMAT)

    TIMEOUT = 20
    GARBAGE = 15
    INFINITY = 16

    def __init__(self, entry):
        self.address_family_identifier = entry[0]
        self.route_tag = entry[1]
        self.ip_address = entry[2]
        self.subnet_mask = entry[3]
        self.next_hop = entry[4]
        self.metric = entry[5]

        self.timeout = time.time() + self.TIMEOUT
        self.garbage_time = self.GARBAGE
        self.changed_flag = False
        self.expired_flag = False

    def set_next_hop(self, next_hop):
        self.next_hop = next_hop

    def set_metric(self, metric):
        self.metric = metric

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def set_subnet_mask(self, subnet_mask):
        self.subnet_mask = subnet_mask

    def pack(self):
        return struct.pack( self.FORMAT,
                            self.address_family_identifier,
                            self.route_tag,
                            int(self.ip_address),
                            int(self.subnet_mask),
                            int(self.next_hop),
                            self.metric)

    def __str__(self):
        metric = "inf"
        if self.metric is not self.INFINITY:
            metric = self.metric

        repr = "|{:^10}|{:^10}|{:^20}|{:^20}|{:^25}|{:^12}| {:^20}| {:^15}| {:^15}| \n"
        return repr.format(self.address_family_identifier,
                self.route_tag,
                format(ipaddress.IPv4Address(self.ip_address)),
                format(ipaddress.IPv4Address(self.subnet_mask)),
                format(ipaddress.IPv4Address(self.next_hop)),
                metric,
                self.expired_flag,
                self.timeout_remaining(),
                self.garbage_remaining()
                )

    def reset_timeout(self):
        self.timeout = time.time() + self.TIMEOUT
        self.garbage_time = self.GARBAGE
        self.changed_flag = False
        self.expired_flag = False

    def expired(self):
        self.metric = self.INFINITY
        self.garbage_time = time.time() + self.GARBAGE
        self.change_flag = True
        self.expired_flag = True

    def timeout_remaining(self):
        if self.expired_flag:
            return 0
        else:
            return int(self.timeout - time.time())

    def garbage_remaining(self):
        if self.expired_flag:
            return int(self.garbage_time - time.time())
        else:
            return self.garbage_time
