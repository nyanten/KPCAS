import os
import cv2

CD = os.getcwd()
REAL_PATH = os.path.join(CD, "image_folder", "take.jpg")


def Camera():
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
    
    while True:
        ret, im = cap.read()
        cv2.imshow('camera capture', im)
        key = cv2.waitKey(10)
        if key == 27:  # esc
            break
        
        if key == 32: # space
            save = cv2.imwrite(REAL_PATH, im)
            print("take a photo")
            
    cap.release()
    cv2.destroyAllWindows()
