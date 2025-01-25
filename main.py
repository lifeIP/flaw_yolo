import cv2
from ultralytics import YOLO


IS_DEBUG = True
ID = 0
MODEL_PATH = "yolov8s.pt"


model = YOLO(MODEL_PATH)


# Подключаемся к камере с индексом 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
else:

    if IS_DEBUG:
        cv2.namedWindow('Video')
        cv2.namedWindow('Controls')
        from src.work_with_trackbars import create_trackbar
        create_trackbar('Controls')
        from src.work_with_trackbars import load_trackbar_value_from_file
        load_trackbar_value_from_file('Controls', ID)


    # Основной цикл обработки кадров
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        
        if IS_DEBUG:
            from src.work_with_trackbars import get_crop_values
            crop_left, crop_right, crop_up, crop_down, confidence_threshold = get_crop_values('Controls')
        else:
            from src.work_with_files import load_settings_from_file
            crop_left, crop_right, crop_up, crop_down, confidence_threshold = load_settings_from_file(0)


        

        if crop_right > crop_left and crop_down > crop_up:
            # Обрезаем изображение в соответствии с полученными значениями
            cropped_frame = frame[crop_up:crop_down, crop_left:crop_right]
            
            detections = model(cropped_frame)[0]

            from src.draw_something import draw_bounding_boxes
            img_with_bounding_boxes = draw_bounding_boxes(cropped_frame.copy(), detections, float(confidence_threshold)/10000)
            
            cv2.imshow('Neuro', img_with_bounding_boxes)
        

        cv2.imshow('Video', frame)
        

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("s"):
            from src.work_with_files import save_settings_into_file
            save_settings_into_file(crop_left, crop_right, crop_up, crop_down, confidence_threshold, ID)

    # Освобождаем ресурсы камеры
    cap.release()
    
    # Закрываем все окна
    cv2.destroyAllWindows()