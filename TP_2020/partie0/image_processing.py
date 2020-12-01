# Image Processing with OpenCV

import cv2
import os
import sys
from matplotlib import pyplot as plt

# Affichier des info de Python
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)

# Affichier la version de opencv
print("OPENCV Version =", cv2.__version__)

# Obtenir le path du fichier python
rep_cour = os.getcwd()
print(rep_cour)

# Lire une image et changer l'image en niveau de gris au travers de cvtColor
img = cv2.imread('data/boats.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# L'opérateur Laplacian est utilisé pour la détection des contours d'une image
laplacian = cv2.Laplacian(img,cv2.CV_64F)

# Le gradient de Sobel est un algorithme pour détecter les contours d'une image avec un noyau
# ici la taille de noyau est 5*5
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

# Visualiser les images dans un graphe
plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
plt.show()