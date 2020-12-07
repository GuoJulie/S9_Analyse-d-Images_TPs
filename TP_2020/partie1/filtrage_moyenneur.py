import image_statistique
import cv2
from matplotlib import pyplot as plt

plt.imshow(image_statistique.img_lisa, 'gray')
dim = (5, 5)
img = cv2.resize(image_statistique.img_lisa, dim)
plt.imshow(image_statistique.img_lisa, 'gray')
plt.show()
