import cv2
import time

from threading import Thread
from flask import Flask

from ObjectDetection.ObjectDetection import ObjectDetection
from Track.HumanTrack import HumanTrack

from Manipulator.Manipulator import Manipulator
from Manipulator.States.Unlocked import Unlocked
from Manipulator.States.Locked import Locked


def robot_thread_task(yolo, webcam_number, track, manipulator):
    # objects_props consits 
    # {obj_class, obj_height, manip_state}
    # manip_state when robot come to this object
    objects_props = [
        {
            # Bottle
            'obj_class': 39,
            'obj_height': 25,
            'manip_state': Locked
        },
        {
            # Person
            'obj_class': 0,
            'obj_height': 160,
            'manip_state': Unlocked
        }
    ]

    iterator = 0
    video = cv2.VideoCapture(webcam_number)

    global robot_is_working
    object_founded = False
    track_status = 'rotating'

    while True:
        if robot_is_working:

            image = video.read()[1]
            info = ''

            if (not object_founded):
                obj_class = objects_props[iterator]['obj_class'],
                obj_height = objects_props[iterator]['obj_height']

                info = 'Finding object class #{}'.format(obj_class)
                image, object_founded, distance_to_bottle, angle_to_bottle = yolo.dectect_object(
                    image,
                    obj_class,
                    obj_height
                )
            else:
                if track_status == 'rotating':
                   info = track.rotate(angle_to_bottle) 
                elif track_status == 'moving':
                   info = track.move(distance_to_bottle)
                else:
                    raise "Unkonown track status"

            cv2.putText(
                img = image, 
                text = info, 
                org = (30, 30),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 1,
                color = (0, 0, 255),
                thickness = 2
            )

            cv2.imshow("Detection", image)
            key = cv2.waitKey(1)

            if key == 32 and object_founded: 
                object_founded = False

                if track_status == 'rotating':
                    track_status = 'moving'
                elif track_status == 'moving':
                    manipulator.change(objects_props[iterator]['manip_state'])
                    iterator = 0 if (iterator == len(objects_props) - 1) else iterator + 1 
                    track_status = 'rotating'            


        elif (robot_is_working == False):
            cv2.destroyAllWindows()
            time.sleep(2)

        else:
            break

    video.release()


if __name__ == "__main__":
    # yolo_weights = r'C:\Users\dimaz\Desktop\storage-automatisation-robot\src\yolo_files\yolov3.weights'
    # yolo_config = r'C:\Users\dimaz\Desktop\storage-automatisation-robot\src\yolo_files\yolov3.cfg'  

    yolo_weights = '/app/src/yolo_files/yolov3.weights'
    yolo_config = '/app/src/yolo_files/yolov3.cfg'    
    
    confidence_threshold = 0.5
    webcam_number = -1
    
    yolo = ObjectDetection(yolo_weights, yolo_config, confidence_threshold)
    track = HumanTrack()
    manipulator = Manipulator()

    app = Flask(__name__)

    robot_is_working = False   

    robot_thread = Thread(
        target = robot_thread_task, 
        args = (yolo, webcam_number, track, manipulator, )
    )
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



    app.run(host="0.0.0.0")
