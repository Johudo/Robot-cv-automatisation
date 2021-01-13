import cv2
import numpy as np


class ObjectDetection(object):

    def __init__(self, yolo_weights, yolo_config, confidence_threshold):
        self.yolo_weights = yolo_weights
        self.yolo_config = yolo_config
        self.confidence_threshold = confidence_threshold

        self.net = cv2.dnn.readNet(yolo_weights, yolo_config)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]


    def perform_detection(self, image, class_number):
        blob = cv2.dnn.blobFromImage(image, 1 / 255., (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)

        h, w = image.shape[:2]

        boxes = []
        
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > self.confidence_threshold and class_id == class_number:
                    center_x, center_y, width, height = list(map(int, detection[0:4] * [w, h, w, h]))

                    top_left_x = int(center_x - (width / 2))
                    top_left_y = int(center_y - (height / 2))

                    boxes.append([top_left_x, top_left_y, width, height])

        return boxes



    def draw_boxes(self, img, box, box_color):
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x + w, y + h), box_color, 2)
                



    def get_distance_to_object(self, box, obj_cm_height):
        obj_pixels_height = box[3]
        camera_koef = 730
        return camera_koef * obj_cm_height / obj_pixels_height



    def get_angle_to_object(self, box, distance_to_object, image_width):
        # delta_x = (box[0] + box[2] / 2) - (image_width / 2)
        # print(delta_x)
        # return np.arcsin(delta_x / distance_to_object)
        return 0



    def dectect_object(self, image, class_number, obj_cm_height):
        distance_to_object = 0
        angle_to_object = 0
        ret = False

        boxes = self.perform_detection(image, class_number)
    
        if (len(boxes) > 0):
            self.draw_boxes(image, boxes[0], (255, 255, 0))
            ret = True
            distance_to_object = self.get_distance_to_object(boxes[0], obj_cm_height)
            angle_to_object = self.get_angle_to_object(boxes[0], distance_to_object, image.shape[1])

        return (image, ret, distance_to_object, angle_to_object)