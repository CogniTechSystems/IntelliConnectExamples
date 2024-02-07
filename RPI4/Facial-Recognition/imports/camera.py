#!/usr/bin/env python3

import cv2
import time

import multiprocessing as mp

class camera():

    def __init__(self, config):

        self.config = config

        self.parent, child = mp.Pipe()
        self.p = mp.Process(target=self.update, args=(child, 0))
        self.p.daemon = True
        self.p.start()

    def end(self):

        self.parent.send(2)

    def update(self, conn, stream):

        cap = cv2.VideoCapture(stream)
        run = True

        while run:
            cap.grab()
            rec_dat = conn.recv()

            if rec_dat == 1:
                ret,frame = cap.read()
                conn.send(frame)

            elif rec_dat ==2:
                cap.release()
                run = False

        conn.close()

    def get(self,resize=None):

        self.parent.send(1)
        frame = self.parent.recv()
        self.parent.send(0)

        if resize == None:
            return frame
        else:
            return self.resize(frame, resize)

    def resize(self, frame, percent=65):

        return cv2.resize(frame,None,fx=percent,fy=percent)
