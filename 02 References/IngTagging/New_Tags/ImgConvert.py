# Image format conversion


# Importing packages
import os
import cv2


def convertPNGtoJPG(file_path):
    newfile_path = file_path
    if os.path.splitext(file_path)[1] == '.png':
        img = cv2.imread(file_path)
        newfile_path = file_path.replace(".png", ".jpg")
        cv2.imwrite(newfile_path, img)
    return newfile_path


def deletePNG_JPG(file_path):
    if os.path.splitext(file_path)[1] == '.png':
        newfile_path = file_path.replace(".png", ".jpg")
        os.remove(newfile_path)
    return file_path