import cv2
import time
import argparse
import numpy as np


def load_input_image(image_path):
    test_img = cv2.imread(image_path)
    h, w, _ = test_img.shape

    return test_img, h, w



def yolov3(yolo_weights, yolo_cfg):
    net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return net, output_layers



def perform_detection(net, img, class_number, output_layers, w, h, confidence_threshold):
    blob = cv2.dnn.blobFromImage(img, 1 / 255., (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    boxes = []
    confidences = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > confidence_threshold and class_id == class_number:
                center_x, center_y, width, height = list(map(int, detection[0:4] * [w, h, w, h]))

                top_left_x = int(center_x - (width / 2))
                top_left_y = int(center_y - (height / 2))

                boxes.append([top_left_x, top_left_y, width, height])
                confidences.append(float(confidence))

    return boxes, confidences



def draw_boxes(boxes, confidences, img, confidence_threshold, NMS_threshold):

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, NMS_threshold)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow("Detection", img)



def dectection_video_file(webcam, yolo_weights, yolo_cfg, class_number, confidence_threshold, nms_threshold):
    net, output_layers = yolov3(yolo_weights, yolo_cfg)

    video = cv2.VideoCapture(webcam)

    while True:
        ret, image = video.read()
        h, w, _ = image.shape
        boxes, confidences = perform_detection(net, image, class_number, output_layers, w, h, confidence_threshold)
        draw_boxes(boxes, confidences, image, confidence_threshold, nms_threshold)

        if cv2.waitKey(1) == 32:
            break

    video.release()
    cv2.destroyAllWindows()


    
    
if __name__ == '__main__':

    YOLO_WEIGHTS = './yolov3.weights'
    YOLO_CONFIG = './yolov3.cfg'
    NEEDED_CLASS_NUM = 39
    WEBCAM_NUMBER = 1

    nms_threshold = 0.4
    confidence_threshold = 0.5

    dectection_video_file(WEBCAM_NUMBER, YOLO_WEIGHTS, YOLO_CONFIG, NEEDED_CLASS_NUM, confidence_threshold, nms_threshold)
