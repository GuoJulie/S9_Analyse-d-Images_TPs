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
    plt.subplot(122)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()

# Afficher l'image d'equalisation
def img_equ(img):
    global equ
    equ = cv2.equalizeHist(img)
    res = np.hstack((img, equ))

    cv2.imshow('img', res)
    cv2.waitKey()
    cv2.destroyAllWindows()

def img_gris(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img

# def img_lisa():
#     rep_cour = os.path.dirname(os.getcwd())
#     path_lisa = rep_cour + '/data/lisa.png'
#
#     return img_gris(path_lisa)

global img_lisa

if __name__ == '__main__':
    # Obtenir le path du fichier python
    rep_cour = os.path.dirname(os.getcwd())
    print(rep_cour)

    path_lisa = rep_cour + '/data/lisa.png'
    path_vache = rep_cour + '/data/vache.jpg'
    path_paysage = rep_cour + '/data/paysage.jpg'
    path_boat = rep_cour + '/data/boats.jpg'
    path_soleil = rep_cour + '/data/soleil.png'
    # Lire une image et changer le couleur en gris au travers de cvtColor

    img_lisa = img_gris(path_lisa)
    img_vache = img_gris(path_vache)
    img_paysage = img_gris(path_paysage)
    img_boat = img_gris(path_boat)
    img_soleil = img_gris(path_soleil)

    img_hist(img_lisa)
    img_hist(img_boat)
    img_equ(img_boat)
    img_hist(img_boat)

