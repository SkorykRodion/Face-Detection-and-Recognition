import cv2
import numpy as np
import os
import re
from FaceDetectorClass import FaceDetector
from VideoStreamClass import VideoStream
from DrawerClass import BBoxDrawer


class FaceCapture():
    def __init__(self, max_samples=20):
        self.max_samples = max_samples
        self.sample_counter = 0
        self.folder_faces = "dataset/"  # where the cropped faces will be stored
        # self.folder_full = "dataset_full/"
        self.final_path = None
        # self.final_path_full = None
        self.name = None


    def create_final_path(self):
        if self.name is not None:
            self.final_path = os.path.sep.join([self.folder_faces, self.name])
            # self.final_path_full = os.path.sep.join([self.folder_full , self.name])

    def set_person_name(self, name):
        self.name = name

    def parse_name(self, name):
        name = re.sub(r"[^\w\s]", '', name)  # Remove all non-word characters (everything except numbers and letters)
        name = re.sub(r"\s+", '_', name)  # Replace all runs of whitespace with a single underscore
        return name

    def create_folders(self):
        if not os.path.exists(self.final_path):
            os.makedirs(self.final_path)
        # if not os.path.exists(self.final_path_full):
        #     os.makedirs(self.final_path_full)

    def process(self):
        video_stream = VideoStream()
        face_detect = FaceDetector()
        drawer = BBoxDrawer()
        self.create_final_path()
        self.create_folders()
        while True:
            status, frame = video_stream.get_frame()
            image = frame.copy()
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
            face_detect.set_input(blob, h, w)
            face_loc = face_detect.get_top_prediction()
            if face_loc is not None:
                counter_tmp = self.sample_counter
                try:
                    start_y, end_y, start_x, end_x = face_loc[0], face_loc[2], face_loc[3], face_loc[1]
                    face_roi = frame[start_y:end_y, start_x:end_x]
                    drawer.set_bbox(image, face_loc)
                    pr_frame = drawer.draw()
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        photo_sample = self.sample_counter + 1
                        image_name = self.name + "." + str(photo_sample) + ".jpg"
                        face_roi = cv2.resize(face_roi, (90, 120))
                        cv2.imwrite(self.final_path + "/" + image_name, face_roi)  # save the cropped face (ROI)

                        #cv2.imwrite(self.final_path_full + "/" + image_name, frame)  # save the full image too (not cropped)
                        cv2.imshow("face", face_roi)
                        self.sample_counter +=1
                except:
                    self.sample_counter = counter_tmp

            else:
                pr_frame = image
            cv2.imshow('frame', pr_frame)
            if self.sample_counter >= self.max_samples:
                cv2.destroyAllWindows()
                video_stream.capture.release()
                del video_stream
                break


