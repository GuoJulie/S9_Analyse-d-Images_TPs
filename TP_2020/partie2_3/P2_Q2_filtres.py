# Image_Processing OpenCV
import cv2
import os
import sys
import numpy as np
from matplotlib import pyplot as plt

#
print("Python version")
print (sys.version)
print (sys.version_info)
print("OPENCV Version =", cv2.__version__)


img = cv2.imread('../data/boats.jpg',0)
source = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Filter box + Normalise
img_box_n = cv2.boxFilter(source, -1, (5, 5), normalize = 1)

# Filter box + not Normalise
img_box = cv2.boxFilter(source, -1, (5, 5), normalize = 0)

# Filter Gaussian
img_gaussian = cv2.GaussianBlur(source, (5, 5), 0)

# Filtre moyenneur
img_moyenneur = cv2.blur(source,(5,5))

# Filtre mdedian
img_mdedian = cv2.medianBlur(source, 5)


#
plt.subplot(2,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,2),plt.imshow(img_box_n,cmap = 'gray')
plt.title('Filter box + Normalise'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,3),plt.imshow(img_box,cmap = 'gray')
plt.title('Filter box + not Normalise'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,4),plt.imshow(img_gaussian,cmap = 'gray')
plt.title('Filter Gaussian'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,5),plt.imshow(img_moyenneur,cmap = 'gray')
plt.title('Filter moyenneur'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,6),plt.imshow(img_mdedian,cmap = 'gray')
plt.title('Filter mdedian'), plt.xticks([]), plt.yticks([])

plt.show()