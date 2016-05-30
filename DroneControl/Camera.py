from Sensor import Sensor
import cv2

class Camera(Sensor):
    def __init__(self):
        self._cap = cv2.VideoCapture(0)

    def read(self):
        return self._cap.read()
