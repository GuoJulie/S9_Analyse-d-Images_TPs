# Mon script OpenCV : Video_processing
import os

import cv2

# retourner une image
def frame_processing(imgc):
     return imgc

rep_cour = os.path.dirname(os.getcwd())
print(rep_cour)

path = rep_cour + '/data/jurassicworld.mp4'

# Lire le vidéo et enregistrer dans une variable cap
cap = cv2.VideoCapture(path)

# Ne pas sortir le boucle while jusqu'à terminer le programme
while (True):

    # Capturer, décoder et retourner la frame suivante
    # ret indique la frame suivante est bien capturée ou pas
    # frame est une matrice des pixels d'image
    ret, frame = cap.read()
    print(ret)
    print(frame)

    # True, la frame est bien capturée
    if ret == True:
        # Copier la frame et changer l'image en niveau de gris utilisant cvtColor
        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Obtenir la frame à afficher
        gray = frame_processing(gray)

        # Affiche la frame originale et la frame en niveau de gris dans la fenêtre
        cv2.imshow('MavideoAvant', frame)
        cv2.imshow('MavideoApres', gray)

    else:
        print('video ended')
        break

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows() 