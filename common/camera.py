import picamera
import numpy as np

class BdCamera:
    RESOLUTION_LO = (320, 160)
    RESOLUTION_MI = (640, 320)
    RESOLUTION_HI = (1280, 640)

    def __init__(self, resolution):
        self.resolution = resolution
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.shutter_speed = 500
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = 1.0

    def rawToGrayscale(self, raw, grayscale):
        grayscale[0::3] = raw[0:raw.size / 3]
        grayscale[1::3] = raw[0:raw.size / 3]
        grayscale[2::3] = raw[0:raw.size / 3]

    def rawToY(self, raw, Y):
        Y = raw[0:raw.size / 3]

    def createEmptyYData(self):
        return np.empty(self.resolution[0] * self.resolution[1], dtype=np.uint8)

    def createEmptyRawData(self):
        return np.empty(self.resolution[0] * self.resolution[1] * 3, dtype=np.uint8)

    def capture(self, data):
        self.camera.capture(data, use_video_port=True, format='yuv')

    def close(self):
        self.camera.close()
