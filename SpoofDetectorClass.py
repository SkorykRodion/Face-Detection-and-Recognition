import cv2
import numpy as np
import tensorflow as tf

class SpoofDetector():
    def __init__(self, model_path='model.h5', threshold=0.9):
        self.model = tf.keras.models.load_model(model_path)
        self.img = None
        self.face_locs = None
        self.threshold = threshold

    def set_image(self, img):
        self.img = img

    def set_face_locs(self, locs):
        self.face_locs = locs

    def get_predictions(self):
        faces = []
        for face in self.face_locs:
            start_y, end_y, start_x, end_x = face[0], face[2], face[3], face[1]
            face_roi = self.img[start_y:end_y, start_x:end_x]

            face_roi= cv2.resize(face_roi, (150, 150))
            face_roi = face_roi / 255.
            face_roi  = face_roi .reshape(-1, 150, 150, 3)
            spoof_pred = self.model.predict(face_roi , verbose=None)
            if (spoof_pred[0] < self.threshold):
                faces.append(True)
            else:
                faces.append(False)
        return np.array(faces)