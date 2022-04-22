"""
Program for putting together a RIP message
Author: Logan Lee
Student ID: 26029766
"""


COMMAND = 0x02  # As always a response packet
VERSION = 0x02  # Version number is always 2 as stated in 4.2 of the assignment specification


class RIPPacket:
    """
    Python class that represents a RIP message
    """

    def __init__(self, src_id):
        """
        Initialises the common header of the RIP message as a byte array
        :param src_id: the source id of the router the packet is being sent from
        """
        if self.is_router_id_valid(src_id):
            self.src_id = src_id
            self.packet = bytearray(4)
            self.packet[0] = COMMAND
            self.packet[1] = VERSION
            self.packet[2] = src_id >> 8
            self.packet[3] = (src_id & 0x00FF)
        else:
            print("Failed to create RIP packet as source router id is invalid")
            raise ValueError

    def rip_packet_entry(self, port_no, next_hop, metric):
        """
        Appends a RIP packet entry onto the common header of the RIP packet and returns it
        :param port_no: port number of input port
        :param next_hop: the router id of the next hop router in the path
        :param metric: the cost metric of the path to the destination
        :return: the RIP packet (byte array) including the common header and packet entry(ies)
        """
        rip_entry = bytearray(20)

        rip_entry[0] = port_no >> 8  # AFI = port number
        rip_entry[1] = port_no & 0x00FF  # AFI = port number

        # Check for the value of the next hop Router ID and print for debugging
        if self.is_router_id_valid(next_hop):
            rip_entry[4] = next_hop >> 24
            rip_entry[5] = (next_hop & 0x00FF0000) >> 16
            rip_entry[6] = (next_hop & 0x0000FF00) >> 8
            rip_entry[7] = (next_hop & 0x000000FF)
        else:
            # Drop entry as invalid next hop router id
            print("Dropped entry as invalid next hop router id")
            return self.packet

        # Check for the value of the metric and print for debugging
        if self.is_metric_valid(metric):
            rip_entry[16] = metric >> 24
            rip_entry[17] = (metric & 0x00FF0000) >> 16
            rip_entry[18] = (metric & 0x0000FF00) >> 8
            rip_entry[19] = (metric & 0x000000FF)
        else:
            # Drop the entry as invalid metric
            print("Dropped the entry as invalid metric")
            return self.packet

        self.packet.extend(rip_entry)
        return self.packet

    def is_router_id_valid(self, router_id):
        """
        Checks to see if the router id valid
        :param router_id: an integer representing the router id
        :return: boolean, true if id is valid, false if not
        """
        return 0 < router_id < 64001

    def is_metric_valid(self, metric):
        """
        Checks to see if the given cost metric is a valid value
        :param metric: integer, the cost metric of a RIP path
        :return: boolean, true if value is valid, false if not
        """
        return 0 < metric < 17


# def main():
#     # Testing
#     test = RIPPacket(1)
#     print(test.packet)
#     print(RIPPacket(64000).packet)
#     # print(RIPPacket(0))
#     # print(RIPPacket(64001))
#
#     print(test.rip_packet_entry(3000, 0, 0))
#     print(test.rip_packet_entry(3000, 1, 17))
#     print(test.rip_packet_entry(3000, 64001, 1))
#     print(test.rip_packet_entry(3000, 1, 1))
#     print(test.rip_packet_entry(3000, 64000, 16))
#
#
# if __name__ == '__main__':
#     main()
