import struct
import ipaddress
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

INFINITY = 16

class RouteEntry:

    FORMAT = "!HHIIII"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, entry):
        self.address_family_identifier = entry[0]
        self.route_tag = entry[1]
        self.ip_address = entry[2]
        self.subnet_mask = entry[3]
        self.next_hop = entry[4]
        self.metric = entry[5]

        self.timeout = None
        self.garbage_time = None
        self.changed_flag = False

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

    def validate_entry(self):
        pass

    def update(self):
        pass

    def __str__(self):
        return (f"{self.address_family_identifier} \t " 
                f"{self.route_tag} \t " 
                f"{format(ipaddress.IPv4Address(self.ip_address))} \t "
                f"{format(ipaddress.IPv4Address(self.subnet_mask))} \t " 
                f"{format(ipaddress.IPv4Address(self.next_hop))} \t " 
                f"{self.metric}\n")
