import cv2
from matplotlib import pyplot as plt
from pandas import np

img = cv2.imread('../data/boats.jpg',0)
source = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Filter box + Normalise
img_box_n = cv2.boxFilter(source, -1, (5, 5), normalize = 1)

# Filter box + not Normalise
img_box = cv2.boxFilter(source, -1, (5, 5), normalize = 0)

# Filter Gaussian
img_gaussian = cv2.GaussianBlur(source, (5, 5), 0)

# Filtre moyenneur
img_moyenneur = cv2.blur(source,(5,5))

# Filtre mdedian
img_mdedian = cv2.medianBlur(source, 5)

# Filter bilateral
img_bilateral = cv2.bilateralFilter(source, 25, 100, 100)

# Filter convolution
kernel = np.ones((9,9), np.float32)/81
img_conv = cv2.filter2D(img, -1, kernel)


#
plt.subplot(3,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,2),plt.imshow(img_box_n,cmap = 'gray')
plt.title('Filter box + Normalise'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,3),plt.imshow(img_box,cmap = 'gray')
plt.title('Filter box + not Normalise'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,4),plt.imshow(img_gaussian,cmap = 'gray')
plt.title('Filter Gaussian'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,5),plt.imshow(img_moyenneur,cmap = 'gray')
plt.title('Filter moyenneur'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,6),plt.imshow(img_mdedian,cmap = 'gray')
plt.title('Filter mdedian'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,7),plt.imshow(img_bilateral,cmap = 'gray')
plt.title('Filter bilateral'), plt.xticks([]), plt.yticks([])

plt.subplot(3,3,8),plt.imshow(img_conv,cmap = 'gray')
plt.title('Filter convolution'), plt.xticks([]), plt.yticks([])

plt.show()