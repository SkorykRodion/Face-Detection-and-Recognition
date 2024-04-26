import cv2
import numpy as np
import os
from PIL import Image
import pickle
import dlib
import sys
import imutils
import face_recognition
import shutil


class Encoder():
    def __init__(self):
        self.training_path = 'dataset/'
        self.pickle_filename = "face_encodings_custom.pickle"

    def get_subdirs(self):
        subdirs = [os.path.join(self.training_path, f) for f in os.listdir(self.training_path)]
        return subdirs

    def get_name(self, dir):
        name = dir.split(os.path.sep)[-1]  # get the name of the subdirectory (which is named after the person)
        name = name.split('/')[-1]
        return name

    def get_img_list(self, dir):
        images_list = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.basename(f).endswith(".jpg")]
        return images_list

    def load_encodings(self):

        list_encodings = []
        list_names = []

        subdirs = self.get_subdirs()

        for subdir in subdirs:
            name = self.get_name(subdir)
            images_list = self.get_img_list(subdir)

            for image_path in images_list:
                img = cv2.imread(image_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                face_roi = face_recognition.face_locations(img, model="cnn")

                img_encoding = face_recognition.face_encodings(img, face_roi)
                if (len(img_encoding) > 0):
                    img_encoding = img_encoding[0]
                    list_encodings.append(img_encoding)
                    list_names.append(name)

        return list_encodings, list_names

    def save(self):
        list_encodings, list_names = self.load_encodings()
        encodings_data = {"encodings": list_encodings, "names": list_names}
        with open(self.pickle_filename, "wb") as f:
            pickle.dump(encodings_data, f)


class EncodingAdapter(Encoder):
    def __init__(self):
        super().__init__()

    def del_dir(self, dir):
        shutil.rmtree(dir)

    def del_person(self, name):
        train_path = self.training_path + name
        self.del_dir(train_path)

    def rename_person(self, old_name, new_name):
        old_path = self.training_path + old_name
        new_path = self.training_path + new_name
        os.rename(old_path, new_path)
        images_list = self.get_img_list(new_path)

        for old_image_path in images_list:
            tmp = old_image_path.split(os.path.sep)
            new_image_path = tmp[0] + os.path.sep + tmp[1].replace(old_name, new_name)
            os.rename(old_image_path, new_image_path)

    def load_persons_preview(self):
        list_persons = []
        subdirs = self.get_subdirs()

        for subdir in subdirs:
            name = self.get_name(subdir)
            images_list = self.get_img_list(subdir)
            image_path = images_list[0]
            list_persons.append((name, image_path))

        return list_persons
