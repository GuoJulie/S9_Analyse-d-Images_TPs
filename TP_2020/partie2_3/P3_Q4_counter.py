import cv2
import numpy as np

img = cv2.imread('../data/cellules.png', 1)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Transformez l'image en image en niveaux de gris
kernel=np.ones((2,2),np.uint8) #Opération d'expansion de corrosion
erosion=cv2.erode(gray,kernel,iterations=5) #expansion
dilation=cv2.dilate(erosion,kernel,iterations=5) #corrosion
ret, thresh = cv2.threshold(dilation, 150, 255, cv2.THRESH_BINARY) # Méthode binaire de traitement de seuil
thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# Filtrage gaussien
contours,hirearchy=cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)# Trouver un domaine connecté
#Comparez la zone des domaines connectés
area=[] #Créez un tableau vide et mettez la zone du domaine connecté
contours1=[]   #Créez un tableau vide et mettez le nombre moins la plus petite zone
for i in contours:
      # area.append(cv2.contourArea(i))
      # print(area)
     if cv2.contourArea(i)>30:  # Calculer la zone Supprimer les domaines connectés avec une petite zone
        contours1.append(i)
print(len(contours1)-1) #Calculez le nombre de domaines connectés
draw=cv2.drawContours(img,contours1,-1,(0,255,0),1) #Délimiter les domaines connectés
#Trouvez le centre de gravité du domaine connecté et dessinez le nombre au point de coordonnées du centre de gravité
for i,j in zip(contours1,range(len(contours1))):
    M = cv2.moments(i)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    draw1=cv2.putText(draw, str(j), (cX, cY), 1,1, (255, 0, 255), 1) #Dessinez des nombres sur le point de coordonnées central

cv2.imshow("draw",draw1)
cv2.imshow("thresh1",thresh1)
cv2.waitKey()
cv2.destroyWindow()
