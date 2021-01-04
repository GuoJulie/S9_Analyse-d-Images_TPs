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


img = cv2.imread('../data/2019010A_0.jpg',0)

#Laplace算子和Sobel算子一样，属于空间锐化滤波操作。
laplacian = cv2.Laplacian(img,cv2.CV_64F)

# sobel算子是一个离散差分算子.它计算图像像素点亮度值的近似梯度.
# 图像是二维的,即沿着宽度/高度两个方向.
# 索贝尔算子是模拟一阶求导,导数越大的地方说明变换越剧烈,越有可能是边缘.
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

#
plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])

plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])

plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()




