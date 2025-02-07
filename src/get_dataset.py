import cv2 


camera_index = 0

camera = cv2.VideoCapture(camera_index)



while True:
    # Захват кадра
    ret, frame = camera.read()
    
    if not ret:
        print(f"Не удалось получить кадр с камеры {camera_index}")
        break
        
    
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    
    # Если нажата клавиша 's', сохраняем кадр
    if key == ord('s'):
        cv2.imshow("dataset", frame)
        filename = f'dataset/{camera_index}_{cv2.getTickCount()}.jpg'
        cv2.imwrite(filename, frame)
        print(f"Сохранено фото: {filename}")

    # Если нажата клавиша 'q', выходим из цикла
    if key == ord('q'):
        break

# Освобождаем камеру и закрываем окно
camera.release()
cv2.destroyWindow(f'Камера {camera_index}')
