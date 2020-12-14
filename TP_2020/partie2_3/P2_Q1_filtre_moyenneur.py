import cv2
import os
import sys
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../data/lisa.png',0)
img5 = cv2.blur(img,(5,5))
img9 = cv2.blur(img,(9,9))
img15 = cv2.blur(img,(15,15))

print("image_shape: ", img.shape)
img_height = img.shape[0]
img_width = img.shape[1]
new_dim = min(img_width,img_height)
img_max = cv2.blur(img,(new_dim,new_dim))

plt.subplot(2,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,2),plt.imshow(img5,cmap = 'gray')
plt.title('5*5'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,3),plt.imshow(img9,cmap = 'gray')
plt.title('9*9'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,4),plt.imshow(img15,cmap = 'gray')
plt.title('15*15'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,5),plt.imshow(img_max,cmap = 'gray')
plt.title(str(new_dim) + '*' + str(new_dim)), plt.xticks([]), plt.yticks([])

plt.show()
