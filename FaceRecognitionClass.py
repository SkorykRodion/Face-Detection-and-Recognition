import pickle

import face_recognition
import numpy as np


class FaceRecognizer():
    def __init__(self, encoding_path="face_encodings_custom.pickle", tolerance=0.6):
        self.tolerance = tolerance
        data_encoding = pickle.loads(open(encoding_path, "rb").read())
        self.list_encodings = data_encoding["encodings"]
        self.face_encodings = []
        self.list_names = data_encoding["names"]
        self.face_locs = []

    def set_image(self, img):
        self.img = img

    def set_face_locs(self, locs):
        self.face_locs = locs

    def encode_faces(self):
        self.face_encodings = face_recognition.face_encodings(self.img, self.face_locs)

    def get_face_matches(self):
        self.encode_faces()
        face_names = []
        conf_values = []
        for encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.list_encodings, encoding, tolerance=self.tolerance)
            name = "Not identified"

            face_distances = face_recognition.face_distance(self.list_encodings, encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.list_names[best_match_index]
            face_names.append(name)
            conf_values.append(face_distances[best_match_index])
        return face_names, conf_values