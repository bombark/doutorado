import os
import cv2
import ufr
from base_camera import BaseCamera


class Camera(BaseCamera):

    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def frames():
        topic = ufr.Link("@new mqtt:topic @host 185.209.160.8 @topic teste @coder msgpack:obj")
        topic.start_subscriber()

        while True:
            # read current frame
            topic.recv()
            image_jpg = topic.read()

            # encode as a jpeg image and return it
            yield image_jpg.tobytes()
