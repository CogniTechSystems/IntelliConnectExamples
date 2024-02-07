
import os
import sys
import time

from imports.confs import confs
from imports.intelliconnect import intelliconnect
from imports.geolocation import geolocation

from imports.openvino import openvino

from imports.read import read
from imports.stream import stream
from imports.sockets import sockets

from threading import Thread

class core():

    def __init__(self):

        config = confs()
        self.configs = config.config

        self.geolocation = geolocation(self.configs)

    def load_intelliconnect(self):
        self.intelliconn = intelliconnect(self.configs, self.geolocation)

    def load_provisioning(self):
        print("Checking device registration status!")
        pclient = self.intelliconn.createProvisioningClient()
        return pclient.register()

    def load_client(self, result):
        print("Connecting to IntelliConnect IoT!")
        self.intelliconn.createDeviceClient(result)
        self.intelliconn.client.connect()
        print("Connected to IntelliConnect IoT!")

    def load_model(self):
        print("Loading model!")
        self.model = openvino(self.configs)
        self.model.load_openvino()
        self.model.load_data()
        print("Model loaded!")

    def serve_model(self, mode=None):
        if mode == "test":
            print("Starting testing!")
            self.model.test()
        else:
            self.sockets = sockets(8282, 8383)
            print("Starting server!")
            Thread(target=read.run, args=(self,), daemon=True).start()
            Thread(target=stream.run, args=(self,), daemon=True).start()

core = core()
core.load_intelliconnect()

def main():

    result = core.load_provisioning()

    if result.status == "assigned":
        print("Device registered!")
        dclient = core.load_client(result)
        core.load_model()
        #core.serve_model("test")
        core.serve_model()

        while True:
            pass

if __name__ == "__main__":
    main()