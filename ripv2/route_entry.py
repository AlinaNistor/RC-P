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

    '''
    FORMAT = "!HHIII"

    def __init__(self):
        self.addressFamilyIdentifier = 2
        self.routeTag = None
        self.ipAddress = None
        self.subnetMask = None
        self.nextHop = None
        self.metric = 1

    def set_route_entry(self, route_entry):
        _route_entry = struct.unpack(self.FORMAT, route_entry)
        self.addressFamilyIdentifier = _route_entry[0]
        self.routeTag = _route_entry[1]
        self.ipAddress = _route_entry[2]
        self.subnetMask = _route_entry[3]
        self.nextHop = _route_entry[4]
        self.metric = _route_entry[5]
