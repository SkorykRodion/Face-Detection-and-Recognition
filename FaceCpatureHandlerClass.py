from FaceCaptureClass import FaceCapture
from EncoderClass import Encoder


class FCDecorator():
    def __init__(self, name):
        self.face_capture = FaceCapture()
        self.face_capture.set_person_name(name)
        self.name = name
        self.encoder = Encoder()

    def run(self):
        self.face_capture.process()
        self.encoder.save()



