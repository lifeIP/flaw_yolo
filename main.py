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




class ManagePThread(QThread):
    
    def __init__(self):
        super().__init__()
        
        self.cam_index_0 = 0 
        self.cam_index_1 = 2
        self.cam_index_2 = 4
        self.cam_index_3 = 6
        self.frame_rate = 5
        self.confidence_threshold = 4500 # 0 - 9999
        

        self.manager = mp.Manager()
        self.mlock = mp.Lock()

        self.array_cam_0 = self.manager.list()
        self.array_cam_1 = self.manager.list()
        self.array_cam_2 = self.manager.list()
        self.array_cam_3 = self.manager.list()
        self.start_or_stop = self.manager.list([False, False])
        self.counts_of_flaws = self.manager.list([0, 0, 0, 0])

        self.start()

    pyqtSlot(bool)
    def slot_start_stop(self, start: bool):
        self.mlock.acquire()
        self.start_or_stop[0] = start
        self.mlock.release()
    
    pyqtSlot(bool)
    def slot_exit_thread(self, exit: bool):
        self.mlock.acquire()
        self.start_or_stop[1] = exit
        self.mlock.release()

    def get_image_from_cam(self, cam_index, array_cam, frame_rate, start_or_stop):
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

            if start_or_stop[1]:
                break

            if not start_or_stop[0]:
                continue

            if not ret:
                break

            cropped_frame = frame[crop_up:crop_down, crop_left:crop_right]
            array_cam.append(cropped_frame)
            
            
            
            time_on_frame = time.time() - start_time
            
            if calculated_time_on_frame - time_on_frame > 0:
                time.sleep(calculated_time_on_frame - time_on_frame)
            
            #TODO: надо реализовать функцию, которая отвечает за переполнение буфера



    def yolo_data_processing(self, array_cam, confidence_threshold, start_or_stop, counts_of_flaws):
        

        while(True):
            if start_or_stop[1]:
                break

            arr = list()

            for img in array_cam:
                arr.append(Image.fromarray(img))
            
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


                directory_with_boxes = f"images/boxes/{datetime.today().strftime('%Y/%m/%d')}"
                file_name = time.time_ns()
                
                for data in obj.boxes.data.tolist():
                    # extract the confidence (i.e., probability) associated with the detection
                    confidence = data[4]

                    if float(confidence) < float(confidence_threshold)/10000:
                        continue


                    if not os.path.exists(directory_with_boxes):
                        os.makedirs(directory_with_boxes)

                    xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                    cv2.rectangle(opencv_array, (xmin, ymin) , (xmax, ymax), (0, 255, 0), 2)
                    
                    cv2.imwrite(f"{directory_with_boxes}/{file_name}.png", opencv_array)


    def run(self):
        thread_0 = mp.Process(target=self.get_image_from_cam, args=(self.cam_index_0, self.array_cam_0, self.frame_rate, self.start_or_stop))
        thread_4 = mp.Process(target=self.yolo_data_processing, args=(self.array_cam_0, self.confidence_threshold, self.start_or_stop, self.counts_of_flaws))
        

        thread_0.start()
        thread_4.start()

        thread_0.join()
        thread_4.join()

    


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

        self.count_of_defects = 0
        self.is_line_start = False

        self.worker_thread = QThread(self)
        self.manage = ManagePThread()
        
        self.initUI()
        self.slot_change_status(1 if self.is_line_start else 0)


    signal_start_or_stop = pyqtSignal(bool)
    signal_close_thread = pyqtSignal(bool)

    pyqtSlot()
    def slot_reset_defects_counter(self):
        self.count_of_defects = 0

    def closeEvent(self, e):
        self.signal_close_thread.emit(True)
        e.accept()
    
    
    def slot_button_stop_or_start_line(self):
        print("Stop/Start")
        self.is_line_start = not self.is_line_start
        self.signal_start_or_stop.emit(self.is_line_start)
        self.slot_change_status(1 if self.is_line_start else 0)

    @pyqtSlot(int)
    def slot_change_status(self, status):
        if status == 1:
            self.label_status.setText("СТАТУС: <b style='color: green;'>РАБОТЕТ</b>")
            self.button_stop_or_start_line.setText("Остановить дефектоскоп")
            self.line_status = 1
        elif status == 0:
            self.label_status.setText("СТАТУС: <b style='color: blue;'>ОСТАНОВЛЕН</b>")
            self.button_stop_or_start_line.setText("Запустить дефектоскоп")
            self.line_status = 0
        elif status == 2:
            self.label_status.setText("СТАТУС: <b style='color: red;'>ОШИБКА</b>")
            self.line_status = 2
            self.button_stop_or_start_line.setText("ПЕРЕЗАГРУЗКА")

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label_count_of_defects_name = QLabel("КОЛИЧЕСТВО ДЕФЕКТОВ")
        label_count_of_defects_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_count_of_defects_name.setFont(QFont(None, 28))


        self.label_count_of_defects = QLabel(f"{self.count_of_defects}")
        self.label_count_of_defects.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_count_of_defects.setFont(QFont(None, 62))


        button_reset_counter = QPushButton("СБРОСИТЬ СЧЕТЧИК")
        button_reset_counter.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        button_reset_counter.setFont(QFont(None, 28))
        button_reset_counter.clicked.connect(self.slot_reset_defects_counter)


        self.label_timer = QLabel("0 сек")
        self.label_timer.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.label_timer.setFont(QFont(None, 28))
        self.label_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.label_status = QLabel("СТАТУС")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setFont(QFont(None, 28))


        placeholder = QWidget()
        placeholder.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)


        self.button_stop_or_start_line = QPushButton()
        self.button_stop_or_start_line.setText("Запустить дефектоскоп")
        self.button_stop_or_start_line.clicked.connect(self.slot_button_stop_or_start_line)
        self.button_stop_or_start_line.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.button_stop_or_start_line.setFont(QFont(None, 28))


        layout_vertical_box_main = QVBoxLayout(self)
        layout_vertical_box_main.addWidget(label_count_of_defects_name, 2)
        layout_vertical_box_main.addWidget(self.label_count_of_defects, 2)
        layout_vertical_box_main.addWidget(button_reset_counter, 1)
        layout_vertical_box_main.addWidget(placeholder, 5)
        layout_vertical_box_main.addWidget(self.label_timer, 1)
        layout_vertical_box_main.addWidget(self.label_status, 2)
        layout_vertical_box_main.addWidget(self.button_stop_or_start_line, 4)

        self.signal_start_or_stop.connect(self.manage.slot_start_stop)
        self.signal_close_thread.connect(self.manage.slot_exit_thread)
        self.manage.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.show()


  

if __name__ == "__main__":
    # Запуск графического приложения
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec()) 
