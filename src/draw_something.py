import cv2 


BOUNDING_BOXES_COLOR = (0, 255, 0)


def draw_bounding_boxes(frame, detections, confidence_threshold):
    for data in detections.boxes.data.tolist():
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]

        # filter out weak detections by ensuring the 
        # confidence is greater than the minimum confidence
        if float(confidence) < confidence_threshold:
            continue

        # if the confidence is greater than the minimum confidence,
        # draw the bounding box on the frame
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax), BOUNDING_BOXES_COLOR, 2)

    return frame