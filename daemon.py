import select
import socket
import sys

from ripPacket import *
from ConfigParser import *

LOCAL_HOST = '127.0.0.1'


class Daemon:
    """
    The daemon program that runs the RIP protocol on the routers
    """
    def __init__(self, config_filename):
        """
        Initialises the router's information: Gets router id, input ports, output ports using the ConfigParser class
        :param config_filename: string, config filename (or file path) of the relevant router for getting routing information
        """
        config = ConfigParser().read_config_file(config_filename)
        self.router_id = config[0]
        self.input_ports = config[1]
        self.outputs = config[2]
        self.input_sockets = self.create_input_sockets()
        self.blocking_time = 1 # only block for 1 second each loop

    def create_input_sockets(self):
        """
        Creates, binds and stores a socket for every input port
        :return: list of sockets
        """
        sockets = []
        for port in self.input_ports:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.bind((LOCAL_HOST, port))
            sockets.append(temp_socket)
        return sockets

    def send_initial_message(self):
        """
        Sends neighbouring routers message with just the RIP packet common header, so they add this router to routing
        tables
        """
        init_packet = RIPPacket(self.router_id)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for port in self.outputs:
            send_socket.connect((LOCAL_HOST, port))
            send_socket.sendall(init_packet)

    def close_sockets(self):
        """
            Closes all open sockets to quit the program
        """
        for socket in self.sockets:
            socket.close()
        self.sockets.clear()

    def receive_packets(self):
        """
            Checks all incoming ports for packets ready to be read. If there are packets, it reads them and interprets the data.
        """

        readable_sockets, _, _ = select.select(self.input_ports, [], [], self.blocking_time)

        for socket in readable_sockets:
            data, _ = socket.recvfrom(4096)
            self.process_packet(data)

    def process_packet(self, data):
        """
            Takes a bytecode array that contains a RIP packet then first checks the data, then, if the routes are applicable to 
            this router (packet came from a router in its output ports), it updates its forwarding table with the new data
            :param data: bytecode array, contains a RIP packet
        """
        print(data)
        print(data.decode("UTF-8"))


def main(config_filename):
    """
        Runs the RIP Daemon
        :param config_filename: string, config filename (or file path) of the relevant router for getting routing information
    """
    daemon = Daemon(config_filename)
    print(daemon.router_id)
    print(daemon.input_ports)
    print(daemon.output_ports)
    daemon.close_sockets()

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Error: You must input exactly one parameter which is the config file name")
    else:
        config_filename = sys.argv[1]
        try:
            main(config_filename)
        except Exception as exception:
            print(exception)
            quit()