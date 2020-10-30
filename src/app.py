import cv2

from ObjectDetection.ObjectDetection import ObjectDetection
from Track.HumanTrack import HumanTrack

from Manipulator.Manipulator import Manipulator
from Manipulator.States.Unlocked import Unlocked
from Manipulator.States.Locked import Locked

if __name__ == "__main__":
    yolo_weights = './yolo_files/yolov3.weights'
    yolo_config = './yolo_files/yolov3.cfg'
    confidence_threshold = 0.5
    webcam_number = 1
    
    yolo = ObjectDetection(yolo_weights, yolo_config, webcam_number, confidence_threshold)
    track = HumanTrack(webcam_number)
    manipulator = Manipulator()


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
