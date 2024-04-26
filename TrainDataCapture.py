import cv2
import numpy as np
import os
import re
from FaceDetectorClass import FaceDetector
from VideoStreamClass import VideoStream
from DrawerClass import BBoxDrawer
import time
def parse_name(name):
    name = re.sub(r"[^\w\s]", '', name) # Remove all non-word characters (everything except numbers and letters)
    name = re.sub(r"\s+", '_', name)    # Replace all runs of whitespace with a single underscore
    return name

# Create the final folder where the photos will be saved (if the path already doesn't exist)
def create_folders(final_path, final_path_full):
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    if not os.path.exists(final_path_full):
        os.makedirs(final_path_full)



folder_faces = "ld_dataset/"      # where the cropped faces will be stored
folder_full = "ld_dataset_full/"  # where will be stored the full photos

data_label = input('Enter label: ')
data_label = parse_name(data_label)

# Join the path (dataset directory + subfolder)
final_path = os.path.sep.join([folder_faces, data_label])
final_path_full = os.path.sep.join([folder_full, data_label])
print("All photos are going to be saved in {}".format(final_path))

create_folders(final_path, final_path_full)


sample = 0          # starting sample
# loop over every frame of the video stream
video_stream = VideoStream()
face_detect = FaceDetector()
drawer = BBoxDrawer()
while True:
    status, frame = video_stream.get_frame()
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
    face_detect.set_input(blob, h, w)
    face_loc = face_detect.get_top_prediction()
    if face_loc is not None:
        start_y, end_y, start_x, end_x = face_loc[0], face_loc[2], face_loc[3], face_loc[1]
        face_roi = frame[start_y:end_y, start_x:end_x]
        drawer.set_bbox(image, face_loc)
        pr_frame = drawer.draw()
        sample = sample+1
        photo_sample = sample
        image_name = data_label + "." + str(photo_sample) + ".jpg"
        cv2.imwrite(final_path + "/" + image_name, face_roi)  # save the cropped face (ROI)
        cv2.imwrite(final_path_full + "/" + image_name, frame)  # save the full image too (not cropped)
    else:
        pr_frame = image
    cv2.imshow('frame', pr_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        video_stream.capture.release()
        del video_stream
        break
    time.sleep(0.02)