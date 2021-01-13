import cv2
from .Track import Track

class HumanTrack(Track):

    def rotate(self, angle):
        return 'Rotate at angle: {}. Press SPACE'.format( angle )

    def move(self, distance):
        return 'Move forward: {} cm. Press SPACE'.format( distance )