import numpy as np
import cv2

class FaceDetector():
    def __init__(self, prototxt_path="deploy.prototxt.txt",
                 model_path = "res10_300x300_ssd_iter_140000.caffemodel", threshold= 0.7):
        self.network = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.h = 120
        self.w = 600
        self.threshold = threshold
        self.input = None
        self.detections = None

    def set_input(self, blob, h, w):
        self.input = blob
        self.network.setInput(blob)
        self.h = h
        self.w = w

    def detect(self):
        if self.input is not None:
            self.detections = self.network.forward()

    def get_face_locations(self):
        self.detect()
        face_locations = []
        if self.detections is not None:
            for i in range(0, self.detections.shape[2]):
                confidence = self.detections[0, 0, i, 2]
                if confidence > self.threshold:
                    bbox = self.detections[0, 0, i, 3:7] * np.array([self.w, self.h, self.w, self.h])
                    (start_x, start_y, end_x, end_y) = bbox.astype("int")
                    if (start_x < 0 or start_y < 0 or end_x > self.w or end_y > self.h):
                        continue
                    else:
                        face_locations.append((start_y, end_x, end_y, start_x))
        return np.array(face_locations)

    def get_top_prediction(self):
        self.detect()
        conf_max = -1
        face_location = None
        if self.detections is not None:
            for i in range(0, self.detections.shape[2]):
                confidence = self.detections[0, 0, i, 2]
                if confidence > conf_max:
                    bbox = self.detections[0, 0, i, 3:7] * np.array([self.w, self.h, self.w, self.h])
                    (start_x, start_y, end_x, end_y) = bbox.astype("int")
                    if (start_x < 0 or start_y < 0 or end_x > self.w or end_y > self.h):
                        face_location = None
                        conf_max = -1
                    else:
                        face_location = (start_y, end_x, end_y, start_x)
                        conf_max = confidence
        return np.array(face_location)