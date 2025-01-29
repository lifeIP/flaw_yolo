import os
import sys
import cv2
from ultralytics import YOLO
import  multiprocessing as mp
import time
from PIL import Image
from datetime import datetime


from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *


IS_DEBUG = True
ID = 0
MODEL_PATH = "yolo11n.pt"


model = YOLO(MODEL_PATH)



def get_image_from_cam(cam_index, array_cam, frame_rate):
    cap = cv2.VideoCapture(cam_index)
    calculated_time_on_frame:float = 1.0 / frame_rate
    
    from src.work_with_files import load_settings_from_file
    crop_left, crop_right, crop_up, crop_down, confidence_threshold = load_settings_from_file(0)

    
    if not cap.isOpened():
        print(f"Не удалось открыть камеру {cam_index}")
        return

    while True:
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break

        cropped_frame = frame[crop_up:crop_down, crop_left:crop_right]
        array_cam.append(cropped_frame)
        
        
        
        time_on_frame = time.time() - start_time
           
        if calculated_time_on_frame - time_on_frame > 0:
            time.sleep(calculated_time_on_frame - time_on_frame)
        
        #TODO: надо реализовать функцию, которая отвечает за переполнение буфера



def yolo_data_processing(array_cam, confidence_threshold):
    

    while(True):
        arr = list()

        for img in array_cam:
            arr.append(Image.fromarray(img))
        print(len(arr))
        if len(arr) == 0: continue
        
        array_cam[:]=[]
        detections = model(arr)

        for obj in detections:
            from src.draw_something import draw_bounding_boxes
            opencv_array = cv2.cvtColor(obj.orig_img, cv2.COLOR_RGB2BGR)
            

            directory_empty = f"images/empty/{datetime.today().strftime('%Y/%m/%d')}"
            
            if not os.path.exists(directory_empty):
                os.makedirs(directory_empty)
            
            cv2.imwrite(f"{directory_empty}/{time.time_ns()}.png", opencv_array)

            draw_bounding_boxes(opencv_array.copy(), obj, float(confidence_threshold)/10000)



class App(QWidget):
    def keyPressEvent(self, event):
        # если нажата клавиша F11
        if event.key() == Qt.Key.Key_F11:
            # если в полный экран 
            if self.isFullScreen():
                # вернуть прежнее состояние
                self.showNormal()
            else:
                # иначе во весь экран
                self.showFullScreen()

        elif event.key() == Qt.Key.Key_Escape:
            self.close()


    def __init__(self):
        super().__init__()

        self.title = 'Дефектоскоп'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480

        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)



        self.show()



  

if __name__ == "__main__":
    manager = mp.Manager()

    array_cam_0 = manager.list()
    array_cam_1 = manager.list()
    array_cam_2 = manager.list()
    array_cam_3 = manager.list()
    
    
    cam_index_0 = 4  
    cam_index_1 = 2
    cam_index_2 = 4
    cam_index_3 = 6
    frame_rate = 5
    confidence_threshold = 4500 # 0 - 9999

    thread_0 = mp.Process(target=get_image_from_cam, args=(cam_index_0, array_cam_0, frame_rate))
    # thread_1 = mp.Process(target=get_image_from_cam, args=(cam_index_1, array_cam_1, frame_rate))
    # thread_2 = mp.Process(target=get_image_from_cam, args=(cam_index_2, array_cam_2, frame_rate))
    # thread_3 = mp.Process(target=get_image_from_cam, args=(cam_index_3, array_cam_3, frame_rate))
    
    
    thread_4 = mp.Process(target=yolo_data_processing, args=(array_cam_0, confidence_threshold))
    # thread_5 = mp.Process(target=yolo_data_processing, args=(array_cam_1, confidence_threshold))
    # thread_6 = mp.Process(target=yolo_data_processing, args=(array_cam_2, confidence_threshold))
    # thread_7 = mp.Process(target=yolo_data_processing, args=(array_cam_3, confidence_threshold))


    thread_0.start()
    # thread_1.start()
    # thread_2.start()
    # thread_3.start()
    
    thread_4.start()
    # thread_5.start()
    # thread_6.start()
    # thread_7.start()


    # Запуск графического приложения
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())


    thread_0.join()
    # thread_1.join()
    # thread_2.join()
    # thread_3.join()
    
    thread_4.join()
    # thread_5.join()
    # thread_6.join()
    # thread_7.join()
 





# if not cap.isOpened():
#     print("Не удалось открыть камеру")
    
# else:
#     if IS_DEBUG:
#         cv2.namedWindow('Video')
#         cv2.namedWindow('Controls')
#         from src.work_with_trackbars import create_trackbar
#         create_trackbar('Controls')
#         from src.work_with_trackbars import load_trackbar_value_from_file
#         load_trackbar_value_from_file('Controls', ID)


#     # Основной цикл обработки кадров
#     while True:
#         ret, frame = cap.read()
        
#         if not ret:
#             break
        
        
#         if IS_DEBUG:
#             from src.work_with_trackbars import get_crop_values
#             crop_left, crop_right, crop_up, crop_down, confidence_threshold = get_crop_values('Controls')
#         else:
#             from src.work_with_files import load_settings_from_file
#             crop_left, crop_right, crop_up, crop_down, confidence_threshold = load_settings_from_file(0)


        

#         if crop_right > crop_left and crop_down > crop_up:
#             # Обрезаем изображение в соответствии с полученными значениями
#             cropped_frame = frame[crop_up:crop_down, crop_left:crop_right]
            
#             detections = model(cropped_frame)[0]

#             from src.draw_something import draw_bounding_boxes
#             img_with_bounding_boxes = draw_bounding_boxes(cropped_frame.copy(), detections, float(confidence_threshold)/10000)
            
#             cv2.imshow('Neuro', img_with_bounding_boxes)
        

#         cv2.imshow('Video', frame)
        

#         key = cv2.waitKey(1)
#         if key == ord("q"):
#             break
#         if key == ord("s"):
#             from src.work_with_files import save_settings_into_file
#             save_settings_into_file(crop_left, crop_right, crop_up, crop_down, confidence_threshold, ID)

#     # Освобождаем ресурсы камеры
#     cap.release()
    
#     # Закрываем все окна
#     cv2.destroyAllWindows()