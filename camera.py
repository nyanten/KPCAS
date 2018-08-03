import os
import cv2
import numpy as np

import func_collection as func

CD = os.getcwd()
REAL_PATH = os.path.join(CD, "image_folder", "take.jpg")

FACE_CASCADE = "/usr/local/Cellar/opencv/3.4.1_5/"\
               "share/OpenCV/haarcascades/"\
               "haarcascade_frontalface_default.xml"

EYE_CASCADE = "/usr/local/Cellar/opencv/3.4.1_5/"\
              "share/OpenCV/haarcascades/"\
              "haarcascade_eye.xml"


def Camera():
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

    face_cascade = cv2.CascadeClassifier(FACE_CASCADE)
    
    while (cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        
        key = cv2.waitKey(10)
        if key == 27:  # esc
            break
        
        if key == 32: # space
            save = cv2.imwrite(REAL_PATH, frame)
            print("take a photo")

        if key == 48:
            for x, y, w, h in face:
                col = (255, 0, 0)
                bd = 2
                cv2.rectangle(frame, (x, y), (x+w, y+h), col, thickness=bd)
        
        cv2.imshow('camera capture', frame)
        
        
    cap.release()
    cv2.destroyAllWindows()


