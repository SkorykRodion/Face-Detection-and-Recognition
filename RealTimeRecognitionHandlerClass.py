import numpy as np
from VideoStreamClass import VideoStream
from FaceDetectorClass import FaceDetector
from FaceRecognitionClass import FaceRecognizer
from DrawerClass import BBoxRecSpoofDrawer
from SpoofDetectorClass import SpoofDetector
import cv2
import time

class RTFRDecorator():
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.resizing = 0.25
        self.face_detector = FaceDetector()
        self.spoof_detector = SpoofDetector()
        self.face_recognizer = FaceRecognizer()
        self.drawer = BBoxRecSpoofDrawer()
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def run(self):
        pass


class RTFRDecoratorVideo(RTFRDecorator):
    def __init__(self, source, to_save=False):
        super().__init__()
        self.source= source
        self.to_save =to_save
        self.save_path = source[:-4] + '_processed' + source[-4:]
        self.writer_init = False
        self.video_stream = VideoStream(max_width=800, max_height=700, source=source)

    def run(self):
        while True:
            status, frame = self.video_stream.get_frame()
            if status == False:
                del self.video_stream
                break
            image = cv2.resize(frame, (0, 0), fx=self.resizing, fy=self.resizing)
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            (h, w) = image.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
            self.face_detector.set_input(blob, h, w)
            face_locations = self.face_detector.get_face_locations()

            face_locations_rescale = face_locations / self.resizing
            face_locations_rescale = face_locations_rescale.astype(int)

            self.face_recognizer.set_image(img_rgb)
            self.face_recognizer.set_face_locs(face_locations)
            face_names, conf_values = self.face_recognizer.get_face_matches()

            self.spoof_detector.set_image(frame)
            self.spoof_detector.set_face_locs(face_locations_rescale)
            spoof_preds = self.spoof_detector.get_predictions()

            self.drawer.set_bbox(frame, face_locations_rescale)
            self.drawer.set_params(face_names, conf_values, spoof_preds)

            pr_frame = self.drawer.draw()
            self.new_frame_time = time.time()
            fps = 1 / (self.new_frame_time - self.prev_frame_time)
            self.prev_frame_time = self.new_frame_time
            fps = int(fps)
            fps = str(fps)

            #pr_frame = cv2.putText(pr_frame, fps, (7, 70), self.font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('Facial Recognition', pr_frame)
            if(self.to_save):
                if self.writer_init == False :
                    self._fourcc = cv2.VideoWriter.fourcc(*'mp4v')
                    (h, w) = pr_frame.shape[:2]
                    self._out = cv2.VideoWriter(self.save_path, self._fourcc, 10,(w, h))
                    self.writer_init = True

                self._out.write(pr_frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.video_stream.capture.release()
                del self.video_stream
                if(self.writer_init == True):
                    self._out.release()
                break
        cv2.destroyAllWindows()


class RTFRDecoratorWebcam(RTFRDecorator):
    def __init__(self):
        super().__init__()
        self.video_stream = VideoStream(max_width=800, max_height=700)

    def run(self):
        while True:
            status, frame = self.video_stream.get_frame()
            image = cv2.resize(frame, (0, 0), fx=self.resizing, fy=self.resizing)
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            (h, w) = image.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
            self.face_detector.set_input(blob, h, w)
            face_locations = self.face_detector.get_face_locations()

            face_locations_rescale = face_locations / self.resizing
            face_locations_rescale = face_locations_rescale.astype(int)

            self.face_recognizer.set_image(img_rgb)
            self.face_recognizer.set_face_locs(face_locations)
            face_names, conf_values = self.face_recognizer.get_face_matches()

            self.spoof_detector.set_image(frame)
            self.spoof_detector.set_face_locs(face_locations_rescale)
            spoof_preds = self.spoof_detector.get_predictions()

            self.drawer.set_bbox(frame, face_locations_rescale)
            self.drawer.set_params(face_names, conf_values, spoof_preds)

            pr_frame = self.drawer.draw()
            self.new_frame_time = time.time()
            fps = 1 / (self.new_frame_time - self.prev_frame_time)
            self.prev_frame_time = self.new_frame_time
            fps = int(fps)
            fps = str(fps)

            #pr_frame = cv2.putText(pr_frame, fps, (7, 70), self.font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('Facial Recognition', pr_frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.video_stream.capture.release()
                del self.video_stream
                break
        cv2.destroyAllWindows()
