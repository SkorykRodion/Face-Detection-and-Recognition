import cv2

class Drawer():
    def __init__(self):
        self.frame = None
        self.face_locs = None

    def set_bbox(self, frame, face_locs):
        self.frame = frame
        self.face_locs = face_locs

    def draw(self):
        pass

class BBoxDrawer(Drawer):
    def draw(self):
        face_loc = self.face_locs
        if face_loc is not None:
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]  # get the coordinates of the bounding box (ROI of the face)
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (20, 255, 0), 4)
        return self.frame

class BBoxRecSpoofDrawer(Drawer):
    def __init__(self):
        super().__init__()
        self.names = None
        self.conf_values = None
        self.spoof_preds = None

    def set_params(self, names, conf_values, spoof_preds):
        self.names = names
        self.conf_values = conf_values
        self.spoof_preds = spoof_preds

    def draw(self):
        for face_loc, name, conf, is_spoof in zip(self.face_locs, self.names, self.conf_values, self.spoof_preds):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[
                3]  # get the coordinates of the bounding box (ROI of the face)
            if is_spoof:
                cv2.putText(self.frame, 'Spoof', (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (20, 0, 255), 2,
                            lineType=cv2.LINE_AA)
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), (20, 0, 255), 4)
            else:
                conf = "{:.8f}".format(conf)
                cv2.putText(self.frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (20, 255, 0), 2,
                            lineType=cv2.LINE_AA)
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), (20, 255, 0), 4)
                if name != "Not identified":
                    cv2.putText(self.frame, conf, (x1, y2 + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (20, 255, 0), 1,
                                lineType=cv2.LINE_AA)

        return self.frame
