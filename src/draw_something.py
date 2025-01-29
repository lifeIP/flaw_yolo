import os
import cv2 
import time
from datetime import datetime

BOUNDING_BOXES_COLOR = (0, 255, 0)

def draw_bounding_boxes(frame, detections, confidence_threshold):
    directory_with_boxes = f"images/boxes/{datetime.today().strftime('%Y/%m/%d')}"
    file_name = time.time_ns()
    
    for data in detections.boxes.data.tolist():
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]

        if float(confidence) < confidence_threshold:
            continue


        if not os.path.exists(directory_with_boxes):
            os.makedirs(directory_with_boxes)

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax), BOUNDING_BOXES_COLOR, 2)
        
        cv2.imwrite(f"{directory_with_boxes}/{file_name}.png", frame)

    return frame