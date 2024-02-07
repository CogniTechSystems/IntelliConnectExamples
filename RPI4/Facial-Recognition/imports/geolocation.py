#!/usr/bin/env python3

import requests
import socket
import re
import uuid

class geolocation():

    def __init__(self, configs):
        self.configs = configs

    def get_ip(self):

        s = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        return ip

    def get_mac(self):
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def get_location(self):
        loc = ["0.0", "0.0"]

        r = requests.get(
            'http://ipinfo.io/json?token='
                + self.configs["ipinfo"])
        data = r.json()

        if "loc" in data:
            loc = data["loc"].split(',')

        return loc