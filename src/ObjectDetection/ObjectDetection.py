import cv2
import numpy as np


class ObjectDetection(object):

    def __init__(self, yolo_weights, yolo_config, webcam, confidence_threshold):
        self.yolo_weights = yolo_weights
        self.yolo_config = yolo_config
        self.webcam = webcam
        self.confidence_threshold = confidence_threshold

        self.net = cv2.dnn.readNet(yolo_weights, yolo_config)
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]



    def load_input_image(self, image_path):
        test_img = cv2.imread(image_path)
        h, w, _ = test_img.shape

        return test_img, h, w



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



    def draw_boxes(self, img, boxes, box_color):
        for i in range( len(boxes) ):
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), box_color, 2)
                
        return img



    def get_distance_to_object(self, box, obj_cm_height):
        obj_pixels_height = box[3]
        camera_koef = 730
        return camera_koef * obj_cm_height / obj_pixels_height



    def get_angle_to_object(self, box, distance_to_object, image_width):
        # delta_x = (box[0] + box[2] / 2) - (image_width / 2)
        # print(delta_x)
        # return np.arcsin(delta_x / distance_to_object)
        return 0



    def dectection_from_webcam(self, class_number, obj_cm_height):

        video = cv2.VideoCapture(self.webcam, cv2.CAP_DSHOW)

        distance_to_object = 0
        angle_to_object = 0

        while True:
            image = video.read()[1]
            
            boxes = self.perform_detection(image, class_number)
            image = self.draw_boxes(image, boxes, (255, 255, 0))

            cv2.imshow("Detection", image)

            key = cv2.waitKey(1)

            if len(boxes) > 0: 
                distance_to_object = self.get_distance_to_object(boxes[0], obj_cm_height)
                angle_to_object = self.get_angle_to_object(boxes[0], distance_to_object, image.shape[1])

                break

            # if key == 32: 
            #     break
            # elif key == 113:
            #     print("SCREENSHOT")
            #     cv2.imwrite('screenshot.png', image)
            

        video.release()

        return (distance_to_object, angle_to_object)
