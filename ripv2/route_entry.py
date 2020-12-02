import struct


class RouteEntry:

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
    FORMAT = "!HHIII"

    def __init__(self):
        self.addressFamilyIdentifier = 2
        self.routeTag = None
        self.ipAddress = None
        self.subnetMask = None
        self.nextHop = None
        self.metric = 1

        self.timeout = None
        self.garbageTime = None
        self.changed = False

    def set_route_entry(self, route_entry):
        _route_entry = struct.unpack(self.FORMAT, route_entry)
        self.addressFamilyIdentifier = _route_entry[0]
        self.routeTag = _route_entry[1]
        self.ipAddress = _route_entry[2]
        self.subnetMask = _route_entry[3]
        self.nextHop = _route_entry[4]
        self.metric = _route_entry[5]

    def set_next_hop(self, nextHop):
        self.nextHop = nextHop

    def set_metric(self, metric):
        self.metric = metric

    def set_ip_address(self, ipAddress):
        self.ipAddress = ipAddress

    def set_subnet_mask(self, subnetMask):
        self.subnetMask = subnetMask

    def pack(self):
        return struct.pack(self.FORMAT, self.addressFamilyIdentifier, self.routeTag, self.ipAddress,
                           self.subnetMask, self.nextHop, self.metric)

    def validate_entry(self):
        pass
