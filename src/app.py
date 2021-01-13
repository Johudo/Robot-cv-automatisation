import cv2
import time

from threading import Thread
from flask import Flask

from ObjectDetection.ObjectDetection import ObjectDetection
from Track.HumanTrack import HumanTrack

from Manipulator.Manipulator import Manipulator
from Manipulator.States.Unlocked import Unlocked
from Manipulator.States.Locked import Locked


def robot_thread_task(yolo, track, manipulator):
    global robot_is_working
    while True:
        if robot_is_working:
            # --------------------------------------------
            # ------------- BOTTLE DETECTION -------------
            # --------------------------------------------

            BOTTLE_CLASS_NUM = 39
            BOTTLE_HEIGHT = 25

            distance_to_bottle, angle_to_bottle = yolo.dectection_from_webcam(BOTTLE_CLASS_NUM, BOTTLE_HEIGHT)
            track.rotate(angle_to_bottle)
            distance_to_bottle, angle_to_bottle = yolo.dectection_from_webcam(BOTTLE_CLASS_NUM, BOTTLE_HEIGHT)
            track.move(distance_to_bottle)

            manipulator.change(Locked)

            # --------------------------------------------
            # ------------- PERSON DETECTION -------------
            # --------------------------------------------

            PERSON_CLASS_NUM = 0
            PERSON_HEIGHT = 160

            distance_to_person, angle_to_person = yolo.dectection_from_webcam(PERSON_CLASS_NUM, PERSON_HEIGHT)
            track.rotate(angle_to_person)
            distance_to_person, angle_to_person = yolo.dectection_from_webcam(PERSON_CLASS_NUM, PERSON_HEIGHT)
            track.move(distance_to_person)

            manipulator.change(Unlocked)

            cv2.destroyAllWindows()
        
        elif (robot_is_working == False):
            time.sleep(2)

        else:
            break

    

if __name__ == "__main__":
    # yolo_weights = r'C:\Users\dimaz\Desktop\storage-automatisation-robot\src\yolo_files\yolov3.weights'
    # yolo_config = r'C:\Users\dimaz\Desktop\storage-automatisation-robot\src\yolo_files\yolov3.cfg'

    yolo_weights = '/app/src/yolo_files/yolov3.weights'
    yolo_config = '/app/src/yolo_files/yolov3.cfg'    
    
    confidence_threshold = 0.5
    webcam_number = 0
    
    yolo = ObjectDetection(yolo_weights, yolo_config, webcam_number, confidence_threshold)
    track = HumanTrack(webcam_number)
    manipulator = Manipulator()

    app = Flask(__name__)

    robot_is_working = False     
    robot_thread = Thread(target=robot_thread_task, args=(yolo, track, manipulator, ))
    robot_thread.start()

    @app.route('/start')
    def start_robot():
        global robot_is_working
        if (robot_is_working == False):
            robot_is_working = True
            return 'Robot was started'
        else:
            return 'Robot was started before'


    
    @app.route('/stop')
    def stop_robot():
        global robot_is_working
        if (robot_is_working == True):
            robot_is_working = False
            return 'Robot was stoped'
        else:
            # # DEVELOPMENT
            # robot_is_working = None
            # return 'Robot\'s proccess was killed'

            # PRODUCTION
            return 'Robot was stopped before'



    app.run(host="0.0.0.0", debug=True)
