import os
import cv2

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
    
    glass = cv2.imread("./image_folder/glass.png")
    
    while True:
        ret, im = cap.read()
        face = face_cascade.detectMultiScale(im)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #dst = cv2.addWeighted(im, 1, glass, 0.8, 0)
        
        key = cv2.waitKey(10)
        if key == 27:  # esc
            break
        
        if key == 32: # space
            save = cv2.imwrite(REAL_PATH, im)
            print("take a photo")

        for x, y, w, h in face:
            col = (255, 0, 0)
            bd = 2
            cv2.rectangle(im, (x, y), (x+w, y+h), col, thickness=bd)
                
        cv2.imshow('camera capture', im)
        
        
    cap.release()
    cv2.destroyAllWindows()
