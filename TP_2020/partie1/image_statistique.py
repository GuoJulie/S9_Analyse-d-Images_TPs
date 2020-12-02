import os
import cv2
from pandas import np
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

# Afficher l'image d'equalisation
def img_equ(img):
    equ = cv2.equalizeHist(img)
    res = np.hstack((img, equ))

    cv2.imshow('img', res)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Obtenir le path du fichier python
    rep_cour = os.path.dirname(os.getcwd())
    print(rep_cour)

    path = rep_cour + '/data/lisa.png'
    # Lire une image et changer le couleur en gris au travers de cvtColor
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # img_hist(img)
    img_equ(img)
