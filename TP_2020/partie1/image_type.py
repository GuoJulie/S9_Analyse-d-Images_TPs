import os
import cv2
from matplotlib import pyplot as plt

# Calculer la graphe d'histogramme représentant la distribution d'intensité d'une image
def img_hist(img):
    plt.subplot(121)
    plt.imshow(img, 'gray')
    plt.xticks([])
    plt.yticks([])
    plt.title("Original")
    plt.subplot(122)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()

if __name__ == '__main__':
    # Obtenir le path du fichier python
    rep_cour = os.getcwd()
    print(rep_cour)

    # Lire une image et changer le couleur en gris au travers de cvtColor
    img = cv2.imread('data/lisa.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_hist(img)
