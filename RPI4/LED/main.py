
import os
import asyncio

from azure.iot.device import MethodResponse

from imports.confs import confs
from imports.intelliconnect import intelliconnect
from imports.geolocation import geolocation

import sys
import time

import RPi.GPIO as GPIO

# LED is connected to GPIO 17
led_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)

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

    def run(self, mode=None):
        if mode == "test":
            print("Starting testing!")
            asyncio.run(self.test())
        else:
            print("Running!")
            GPIO.output(led_pin, GPIO.HIGH)
            while True:
                time.sleep(1.0)

    def test(self):
        while True:
            GPIO.output(led_pin, GPIO.HIGH)
            print("LED on!")
            self.intelliconn.send_message("ON")
            time.sleep(5.0)
            GPIO.output(led_pin, GPIO.LOW)
            print("LED off!")
            self.intelliconn.send_message("OFF")
            time.sleep(5.0)

    def method_request_handler(self, method_request):
        print("")
        print("IntelliConnect command received!")
        print(method_request.payload)
        print("")
        if method_request.name == "state":
            if(method_request.payload["state"]=="ON"):
                print("Turning LED on!")
                GPIO.output(led_pin, GPIO.HIGH)
                print("LED on!")
                self.intelliconn.send_message("ON")
                payload = {"result": True, "state": "ON"}
                status = 200
            else:
                print("Turning LED off!")
                GPIO.output(led_pin, GPIO.LOW)
                print("LED off!")
                self.intelliconn.send_message("OFF")
                payload = {"result": True, "state": "OFF"}
                status = 200
        else:
            payload = {"result": False, "data": "unknown method"}
            status = 400
            print("Executed unknown method: " + method_request.name)

        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        core.intelliconn.client.send_method_response(method_response)

core = core()
core.load_intelliconnect()

def main():

    result = core.load_provisioning()

    if result.status == "assigned":
        print("Device registered!")
        dclient = core.load_client(result)

        core.intelliconn.client.on_method_request_received  = core.method_request_handler

        #core.run("test")
        core.run()

if __name__ == "__main__":
    main()
