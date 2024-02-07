#!/usr/bin/env python3

import base64
import cv2
import time
import asyncio

from datetime import datetime
from threading import Thread

from imports.camera import camera

class read(Thread):

    def __init__(self):
        pass

    def run(self):

        msg = ""

        self.camera = camera(self.configs)
        self.publishes = [None] * (len(self.model.faces_database) + 1)

        soc = self.sockets.connect()

        while True:
            try:
                frame = self.camera.get()
                detections = self.model.predict(frame)

                cv2.putText(frame, "Innvo8 Camera", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0,0,0), 1, cv2.LINE_AA)

                cv2.putText(frame, str(datetime.now()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.3, (0,0,0), 1, cv2.LINE_AA)

                if len(detections):
                    for roi, landmarks, identity in zip(*detections):
                        frame, label = self.model.draw_detection(frame, roi, identity, landmarks)

                        if label is "Unknown":
                            label = 0
                            msg = "AI identified intruder"
                        else:
                            msg = "AI identified User #" + str(label)

                        print(msg)

                        if (self.publishes[int(label)] is None or (self.publishes[int(label)] + (1 * 120)) < time.time()):
                            self.publishes[int(label)] = time.time()
                            self.intelliconn.send_message(label)

                encoded, buffer = cv2.imencode('.jpg', frame)
                soc.send(base64.b64encode(buffer))

            except KeyboardInterrupt:
                self.lcv.release()
                break
