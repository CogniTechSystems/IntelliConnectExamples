#!/usr/bin/env python3

import json
import os

class confs():

    def __init__(self):

        self.config = {}
        self.load()

    def load(self):

        with open(os.path.dirname(
            os.path.abspath(__file__)) + '/../config/config.json') as config:
            self.config = json.loads(config.read())
