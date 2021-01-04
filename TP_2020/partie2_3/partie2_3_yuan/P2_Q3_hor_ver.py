import cv2
import numpy as np
from matplotlib import pyplot as plt

def trait_horizontaux(path):
    img = cv2.imread(path,0)

    # Noyau de convolution
    con = np.array([[1, 1, 1],
                    [0, 0, 0],
                    [-1, -1, -1]])
    img_con = cv2.filter2D(img, -1, con)

    return img, img_con

def trait_verticaux(path):
    img = cv2.imread(path,0)

    # Noyau de convolution
    con = np.array([[1, 0, -1],
                    [1, 0, -1],
                    [1, 0, -1]])
    img_con = cv2.filter2D(img, -1, con)

    return img, img_con

if __name__=="__main__":
    path_suzan = '../data/suzan.jpg'
    path_zebre = '../data/zebre.jpg'
    trait_horizontaux(path_zebre)
    trait_verticaux(path_zebre)
    trait_horizontaux(path_suzan)
    trait_verticaux(path_suzan)

    plt.subplot(2, 3, 1),plt.imshow(trait_horizontaux(path_zebre)[0], cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])

    plt.subplot(2, 3, 2),plt.imshow(trait_horizontaux(path_zebre)[1], cmap = 'gray')
    plt.title('img_con_horizontale'), plt.xticks([]), plt.yticks([])

    plt.subplot(2, 3, 3),plt.imshow(trait_verticaux(path_zebre)[1], cmap = 'gray')
    plt.title('img_con_vertical'), plt.xticks([]), plt.yticks([])

    plt.subplot(2, 3, 4), plt.imshow(trait_horizontaux(path_suzan)[0], cmap='gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])

    plt.subplot(2, 3, 5), plt.imshow(trait_horizontaux(path_suzan)[1], cmap='gray')
    plt.title('img_con_horizontale'), plt.xticks([]), plt.yticks([])

    plt.subplot(2, 3, 6), plt.imshow(trait_verticaux(path_suzan)[1], cmap='gray')
    plt.title('img_con_vertical'), plt.xticks([]), plt.yticks([])

    plt.show()
