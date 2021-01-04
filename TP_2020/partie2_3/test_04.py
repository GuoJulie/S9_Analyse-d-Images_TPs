#encoding:utf-8

#
#灰度图像直方图
#

from matplotlib import pyplot as plt
import cv2

image = cv2.imread('../data/2019010K_0.tiff')
cv2.imshow("Original",image)

#图像直方图
hist = cv2.calcHist([image],[0],None,[256],[0,256])

plt.figure()#新建一个图像
plt.title("Grayscale Histogram")#图像的标题
plt.xlabel("Bins")#X轴标签
plt.ylabel("# of Pixels")#Y轴标签
plt.plot(hist)#画图
plt.xlim([0,256])#设置x坐标轴范围
plt.show()#显示图像


# -------------------------------------------------------------

#encoding:utf-8

#
#图像直方图均衡化
#

import numpy as np

image = cv2.imread('../data/2019010K_0.tiff',0)#读取灰度图像
cv2.imshow("Original",image)
cv2.waitKey(0)

eq = cv2.equalizeHist(image)#灰度图像直方图均衡化
cv2.imshow("Histogram Equalization", np.hstack([image, eq]))
cv2.waitKey(0)