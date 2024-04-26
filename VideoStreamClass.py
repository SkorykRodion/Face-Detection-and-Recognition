from threading import Thread
import cv2
import time
class VideoCaptureException(Exception):
    pass


class WrongVidFormat(VideoCaptureException):
    def __init__(self, path, message="Video format is not .mp4"):
        self.salary = path
        self.message = message
        super().__init__(self.message)


class CameraError(VideoCaptureException):
    def __init__(self, message="Opening camera error"):
        self.message = message
        super().__init__(self.message)




class VideoStream():

    def __init__(self, max_width = 900,max_height=500, source=None):
        self.max_width = max_width
        self.max_height = max_height
        if source == None:
            self.infinite = True
            self.capture = cv2.VideoCapture(0)
        elif self.is_mp4(source):
            self.infinite = False
            self.capture = cv2.VideoCapture(source)
        else:
            raise WrongVidFormat(source)
        if not self.capture.isOpened():
            raise CameraError()
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.status=True
        time.sleep(1)


    @staticmethod
    def is_mp4(path):
        if path[-4:] == '.mp4':
            return True
        return False
# читання кадрів у іншому потоці
    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            else:
                break
            time.sleep(.02)

    def is_inf(self):
        return self.infinite

    def get_frame(self):
        status_tmp = self.status
        frame_tmp = self.frame
        video_width, video_height = self.resize_video(frame_tmp.shape[1], frame_tmp.shape[0])
        frame_tmp = cv2.resize(frame_tmp, (video_width, video_height))
        return status_tmp, frame_tmp

# зміна розмірів відео з збереженням пропорцій, якщо відео виходить за заначені рамки
    def resize_video(self, width, height):

        video_width = width
        video_height = height
        proportion = width / height
        if self.max_width is not None:
            if width > self.max_width:

                video_width = self.max_width
                video_height = int(video_width / proportion)

        if self.max_height is not None:
            if height > self.max_height:
                video_height = self.max_height
                video_width = int(proportion*video_height)

        return video_width, video_height

    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()
