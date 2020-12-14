import cv2
import os
import pylab
import sys
import numpy as np
from matplotlib import pyplot as plt

def trait_horizontaux():

    img = cv2.imread('../data/zebre.jpg',0)

    # Noyau de convolution
    con = np.array([[1, 1, 1],
                    [0, 0, 0],
                    [-1, -1, -1]])

    img_con = cv2.filter2D(img, -1, con)

    plt.subplot(1,2,1),plt.imshow(img,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])

    plt.subplot(1,2,2),plt.imshow(img_con,cmap = 'gray')
    plt.title('img_con_horizontaux'), plt.xticks([]), plt.yticks([])

    plt.show()

def trait_verticaux():

    img = cv2.imread('../data/suzan.jpg',0)

    # Noyau de convolution
    con = np.array([[1, 0, -1],
                    [1, 0, -1],
                    [1, 0, -1]])

    img_con = cv2.filter2D(img, -1, con)

    plt.subplot(1,2,1),plt.imshow(img,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])

    plt.subplot(1,2,2),plt.imshow(img_con,cmap = 'gray')
    plt.title('img_con_verticaux'), plt.xticks([]), plt.yticks([])

    plt.show()


if __name__=="__main__":
    trait_horizontaux()
    trait_verticaux()