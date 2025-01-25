import cv2
from ultralytics import YOLO



MODEL_PATH = "yolov8s.pt"
GREEN = (0, 255, 0)

model = YOLO(MODEL_PATH)



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
        cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax), GREEN, 2)

    return frame


def on_trackbar_change(value):
    pass

# Подключаемся к камере с индексом 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
else:

    # Создаем основное окно для отображения видео
    cv2.namedWindow('Video')
    
    # Создаем дополнительное окно для трекбаров
    cv2.namedWindow('Controls')
    
    # Создаем трекбары для обрезки
    cv2.createTrackbar('Crop Left', 'Controls', 1, 640, on_trackbar_change)
    cv2.createTrackbar('Crop Right', 'Controls', 639, 640, on_trackbar_change)
    cv2.createTrackbar('Crop Up', 'Controls', 1, 480, on_trackbar_change)
    cv2.createTrackbar('Crop Down', 'Controls', 479, 480, on_trackbar_change)
    cv2.createTrackbar('Confidence Threshold', 'Controls', 9998, 9999, on_trackbar_change)


    from manage_service_data import get_service_data_from_file
    cv2.setTrackbarPos('Crop Left', 'Controls', int(get_service_data_from_file("crop_left")))
    cv2.setTrackbarPos('Crop Right', 'Controls', int(get_service_data_from_file("crop_right")))
    cv2.setTrackbarPos('Crop Up', 'Controls', int(get_service_data_from_file("crop_up")))
    cv2.setTrackbarPos('Crop Down', 'Controls', int(get_service_data_from_file("crop_down")))
    cv2.setTrackbarPos('Confidence Threshold', 'Controls', int(get_service_data_from_file("confidence_threshold")))


    # Основной цикл обработки кадров
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Получаем значения трекбаров
        crop_left = cv2.getTrackbarPos('Crop Left', 'Controls')
        crop_right = cv2.getTrackbarPos('Crop Right', 'Controls')
        crop_up = cv2.getTrackbarPos('Crop Up', 'Controls')
        crop_down = cv2.getTrackbarPos('Crop Down', 'Controls')
        confidence_threshold = cv2.getTrackbarPos('Confidence Threshold', 'Controls')
        

        if crop_right > crop_left and crop_down > crop_up:
            # Обрезаем изображение в соответствии с полученными значениями
            cropped_frame = frame[crop_up:crop_down, crop_left:crop_right]
            

            detections = model(cropped_frame)[0]
            img_with_bounding_boxes = draw_bounding_boxes(cropped_frame.copy(), detections, float(confidence_threshold)/10000)
            cv2.imshow('Neuro', img_with_bounding_boxes)
            

        cv2.imshow('Video', frame)
        
        # Проверяем нажатие клавиши ESC для выхода
        key = cv2.waitKey(1)
        if key == 27:  # Код клавиши ESC
            break
        if key == ord("s"):
            from manage_service_data import set_service_data_into_file
            set_service_data_into_file("crop_left", crop_left)
            set_service_data_into_file("crop_right", crop_right)
            set_service_data_into_file("crop_up", crop_up)
            set_service_data_into_file("crop_down", crop_down)
            set_service_data_into_file("confidence_threshold", confidence_threshold)

    # Освобождаем ресурсы камеры
    cap.release()
    
    # Закрываем все окна
    cv2.destroyAllWindows()