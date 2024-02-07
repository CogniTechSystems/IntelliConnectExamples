#!/usr/bin/env python3

import cv2
import os
import os.path as osp
import time

import numpy as np

from openvino.runtime import Core, get_version

from model.OpenVINO.utils import crop
from model.OpenVINO.landmarks_detector import LandmarksDetector
from model.OpenVINO.face_detector import FaceDetector
from model.OpenVINO.faces_database import FacesDatabase
from model.OpenVINO.face_identifier import FaceIdentifier

from openvino.model_zoo.model_api.models import OutputTransform

class openvino():

    def __init__(self, config):

        self.configs = config
        self.qs = 16
        self.allow_grow = False

    def load_openvino(self):

        core = Core()

        self.face_detector = FaceDetector(core, os.path.dirname(os.path.abspath(__file__)) + '/../' + self.configs["openvino"]["detection"],
                                        input_size=[300, 300],
                                        confidence_threshold=0.6,
                                        roi_scale_factor=1.15)

        self.landmarks_detector = LandmarksDetector(core, os.path.dirname(os.path.abspath(__file__)) + '/../' + self.configs["openvino"]["landmarks"])

        self.face_identifier = FaceIdentifier(core, os.path.dirname(os.path.abspath(__file__)) + '/../' + self.configs["openvino"]["reidentification"],
                                            match_threshold=0.3,
                                            match_algo='HUNGARIAN')

        self.face_detector.deploy(self.configs["openvino"]["runas"])
        self.landmarks_detector.deploy(self.configs["openvino"]["runas"], self.qs)
        self.face_identifier.deploy(self.configs["openvino"]["runas"], self.qs)

        print("OpenVINO loaded")

    def load_data(self):

        self.faces_database = FacesDatabase(os.path.dirname(os.path.abspath(__file__)) + '/../' + \
                                            self.configs["openvino"]["known"], self.face_identifier,
                                            self.landmarks_detector,
                                            self.face_detector, True)
        self.face_identifier.set_faces_database(self.faces_database)
        print('Database is loaded, registered {} identities'.format(len(self.faces_database)))

    def predict(self, frame):

        rois = self.face_detector.infer((frame,))
        if self.qs < len(rois):
            print('Too many faces for processing. Will be processed only {} of {}'
                        .format(self.qs, len(rois)))
            rois = rois[:self.qs]

        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        if self.allow_grow and len(unknowns) > 0:
            for i in unknowns:
                # This check is preventing asking to save half-images in the boundary of images
                if rois[i].position[0] == 0.0 or rois[i].position[1] == 0.0 or \
                    (rois[i].position[0] + rois[i].size[0] > orig_image.shape[1]) or \
                    (rois[i].position[1] + rois[i].size[1] > orig_image.shape[0]):
                    continue
                crop_image = crop(orig_image, rois[i])
                name = self.faces_database.ask_to_save(crop_image)
                if name:
                    id = self.faces_database.dump_faces(crop_image, face_identities[i].descriptor, name)
                    face_identities[i].id = id

        return [rois, landmarks, face_identities]

    def draw_text_with_background(self, frame, text, origin,
                                    font=cv2.FONT_HERSHEY_SIMPLEX, scale=1.0,
                                    color=(0, 0, 0), thickness=1, bgcolor=(255, 255, 255)):
        text_size, baseline = cv2.getTextSize(text, font, scale, thickness)
        cv2.rectangle(frame,
                        tuple((origin + (0, baseline)).astype(int)),
                        tuple((origin + (text_size[0], -text_size[1])).astype(int)),
                        bgcolor, cv2.FILLED)
        cv2.putText(frame, text,
                    tuple(origin.astype(int)),
                    font, scale, color, thickness)
        return text_size, baseline

    def draw_detection(self, frame, roi, identity, landmarks):

        label = self.face_identifier.get_identity_label(identity.id)

        # Draw face ROI border
        cv2.rectangle(frame, tuple(roi.position.astype(int)), tuple(roi.position.astype(int) + roi.size.astype(int)), (0, 220, 0), 2)

        # Draw identity label
        text_scale = 0.5
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize("H1", font, text_scale, 1)
        line_height = np.array([0, text_size[0][1]])
        if label is "Unknown":
            text = str(label)
        else:
            text = "User #" + str(label)
        if identity.id != FaceIdentifier.UNKNOWN_ID:
            text += ' %.2f%%' % (100.0 * (1 - identity.distance))
        self.draw_text_with_background(frame, text,
                                    roi.position - line_height * 0.5,
                                    font, scale=text_scale)

        return frame, label

    def test(self):

        totaltime = 0
        files = 0

        tp = 0
        fp = 0
        tn = 0
        fn = 0
        prediction = 0

        for testFile in os.listdir(self.configs["openvino"]["test"]):
            if os.path.splitext(testFile)[1] in [".jpg"]:

                fileName = self.configs["openvino"]["test"] + "/" + testFile
                frame = cv2.imread(fileName)

                start = time.time()
                detections = self.predict(frame)
                end = time.time()
                benchmark = end - start
                totaltime += benchmark

                for roi, landmarks, identity in zip(*detections):
                    label = self.face_identifier.get_identity_label(identity.id)

                    if label is "Unknown":
                        label = 0
                        mesg = "TassAI identified intruder in " + str(benchmark) + " seconds."
                    else:
                        mesg = "TassAI identified User #" + str(label) + " in " + str(benchmark) + " seconds."

                    print(mesg)

        print("Total Time Taken: " + str(totaltime))
        print("Program exiting")

        exit()
