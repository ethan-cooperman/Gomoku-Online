import socket
import pickle
import bz2
import os


class Network:
    def __init__(self):
        """constructor for the network class
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv('SERVER_IP')
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        """gets the current player
        """
        return self.p

    def connect(self):
        """makes the initial connection between the client and server

        :return: initialization data from the server
        """
        print(self.addr)
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2 ** 30))
        except:
            print('Connection failed')
            pass

    def send(self, data):
        """send data to the server and receive a response

        :param data: the data from the client to be sent
        :return: data from the server based on the initial data
        """
        try:
            self.client.sendall(pickle.dumps(data))
            return pickle.loads(bz2.decompress(self.client.recv(2 ** 30)))
        except socket.error as e:
            print('could not send on Network')
            print(e)
