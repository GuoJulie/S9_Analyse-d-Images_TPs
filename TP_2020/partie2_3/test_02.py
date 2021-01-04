# Mon script OpenCV : Video_processing
#
import numpy as np
import cv2
#
from TP_2020.partie1.video_processing import frame_processing


def imgproc(imgc):
    return imgc
#
cap = cv2.VideoCapture('../data/starwar.mp4')
#
while (True):
    #
    ret, frame = cap.read()
    #
    if ret == True:
        #
        img = frame.copy()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #
        gray = frame_processing(gray)
        #
        cv2.imshow('MavideoAvant', frame)
        cv2.imshow('MavideoApres', gray)
    else:
        print('video ended')
        break

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()