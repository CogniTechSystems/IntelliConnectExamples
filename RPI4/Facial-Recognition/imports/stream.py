#!/usr/bin/env python3

import cv2
import base64
import time
import zmq
import errno
import socket

import numpy as np

from PIL import Image
from io import BytesIO

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread

class stream(Thread):

    def __init__(self):
        pass

    def run(self):

        global capture

        # Subscribes to the socket server
        capture = self.sockets.subscribe()

        try:
            server = ThreadedHTTPServer(
                (self.sockets.ip, int(self.sockets.serverport)), CamHandler)
            print(
                "Camera server started on " + self.sockets.ip+":"+str(self.sockets.serverport))
            server.serve_forever()
        except KeyboardInterrupt:
            server.socket.close()
            capture.close()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('.mjpg'):
                    self.send_response(200)
                    self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
                    self.end_headers()
                    count = 0

                    while True:
                        frame = capture.recv_string()
                        frame = cv2.imdecode(
                            np.fromstring(base64.b64decode(frame),
                            dtype=np.uint8), 1)

                        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        jpg = Image.fromarray(imgRGB)
                        tmpFile = BytesIO()
                        jpg.save(tmpFile,'JPEG')
                        self.wfile.write("--jpgboundary".encode())
                        self.send_header('Content-type','image/jpeg')
                        self.send_header('Content-length',str(tmpFile.getbuffer().nbytes))
                        self.end_headers()
                        self.wfile.write(tmpFile.getvalue())
                    return
        except IOError as e:
            print("Broken Pipe")
