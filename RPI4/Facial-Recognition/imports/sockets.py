#!/usr/bin/env python3

import zmq
import base64
import socket

import numpy as np

class sockets():

    def __init__(self, port, serverport):

        self.ip = self.get_ip()
        self.port = port
        self.serverport = serverport

    def get_ip(self):

        s = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        return ip

    def connect(self):

        try:
            soc = zmq.Context().socket(zmq.PUB)
            soc.connect("tcp://"+self.ip+":"+str(self.port))
            print(
                "Started & connected to socket server: tcp://" \
                +self.ip+":"+str(self.port))
            return soc
        except:
            print(
                "Failed to connect to socket server: tcp://" \
                + self.ip+":"+str(self.port))

    def subscribe(self):

        try:
            context = zmq.Context()
            rsoc = context.socket(zmq.SUB)
            rsoc.setsockopt(zmq.CONFLATE, 1)
            rsoc.bind("tcp://"+self.ip+":"+str(self.port))
            rsoc.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
            print(
                "Subscribed to socket: tcp://" \
                +self.ip+":"+str(self.port))
            return rsoc
        except:
            print(
                "Failed to connect to tcp://" \
                +self.ip+":"+str(self.port))
