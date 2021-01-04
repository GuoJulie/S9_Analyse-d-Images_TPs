import cv2
from matplotlib import pyplot as plt

img_1 = cv2.imread('../data/jeu1.jpg', 0)
img_2 = cv2.imread('../data/jeu2.jpg', 0)
img_3 = cv2.imread('../data/jeu3.jpg', 0)

sp_1 = img_1.shape
crop_size = (sp_1[1], sp_1[0])
img_2 = cv2.resize(img_2, crop_size, interpolation = cv2.INTER_CUBIC)
img_3 = cv2.resize(img_3, crop_size, interpolation = cv2.INTER_CUBIC)
img_subtract_1 = cv2.subtract(img_1,img_2)
img_subtract_2 = cv2.bitwise_xor(img_1,img_3)
img_subtract_3 = cv2.bitwise_xor(img_2,img_3)
ret_1,img_thresh_1 = cv2.threshold(img_subtract_1,127,255,cv2.THRESH_BINARY)
ret_2,img_thresh_2 = cv2.threshold(img_subtract_2,127,255,cv2.THRESH_BINARY)
ret_3,img_thresh_3 = cv2.threshold(img_subtract_3,127,255,cv2.THRESH_BINARY)
titles = ['jeu1 (380,442)','jeu2 (380,442)','jeu3 (383,442)',"jeu1-jeu2 (Différence d'image)","jeu1-jeu3 (Décalage d'image)","jeu2-jeu3 (Décalage d'image)"]
images = [img_1, img_2, img_3, img_thresh_1, img_thresh_2, img_thresh_3]
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


