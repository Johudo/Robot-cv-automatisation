import cv2
from .Track import Track

class HumanTrack(Track):

    def __init__(self, webcam):
        self.webcam = webcam

    
    def rotate(self, angle):
        print('Rotate at angle: {}'.format( angle ))
        self.wait_motion()


    def move(self, distance):
        print('Move forward: {} cm'.format( distance ))
        self.wait_motion()

    
    def wait_motion(self):
        video = cv2.VideoCapture(self.webcam, cv2.CAP_DSHOW)

        while True:
            image = video.read()[1]
            cv2.imshow("Detection", image)

            key = cv2.waitKey(1)

            if key == 32: 
                break
        
        video.release()
