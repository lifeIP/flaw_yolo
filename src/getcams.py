import cv2 as cv

# получаем список всех камер
ids = list()
for i in range(100):
    try:
        cap = cv.VideoCapture(i)
        ret, src = cap.read()
        if ret:
            ids.append(i)
            cap.release()
    except:
        pass


print(ids)