import cv2


def on_trackbar_change(value):
    pass

def get_crop_values(control_window_name):
    crop_left = cv2.getTrackbarPos('Crop Left', control_window_name)
    crop_right = cv2.getTrackbarPos('Crop Right', control_window_name)
    crop_up = cv2.getTrackbarPos('Crop Up', control_window_name)
    crop_down = cv2.getTrackbarPos('Crop Down', control_window_name)
    confidence_threshold = cv2.getTrackbarPos('Confidence Threshold', control_window_name)
    return crop_left, crop_right, crop_up, crop_down, confidence_threshold

def create_trackbar(control_window_name, on_trackbar_change=on_trackbar_change):
    cv2.createTrackbar('Crop Left', control_window_name, 1, 640, on_trackbar_change)
    cv2.createTrackbar('Crop Right', control_window_name, 639, 640, on_trackbar_change)
    cv2.createTrackbar('Crop Up', control_window_name, 1, 480, on_trackbar_change)
    cv2.createTrackbar('Crop Down', control_window_name, 479, 480, on_trackbar_change)
    cv2.createTrackbar('Confidence Threshold', control_window_name, 9998, 9999, on_trackbar_change)

def load_trackbar_value_from_file(control_window_name, id: int = 0):
    from manage_service_data import get_service_data_from_file
    cv2.setTrackbarPos('Crop Left', control_window_name, int(get_service_data_from_file("crop_left", id)))
    cv2.setTrackbarPos('Crop Right', control_window_name, int(get_service_data_from_file("crop_right", id)))
    cv2.setTrackbarPos('Crop Up', control_window_name, int(get_service_data_from_file("crop_up", id)))
    cv2.setTrackbarPos('Crop Down', control_window_name, int(get_service_data_from_file("crop_down", id)))
    cv2.setTrackbarPos('Confidence Threshold', control_window_name, int(get_service_data_from_file("confidence_threshold", id)))