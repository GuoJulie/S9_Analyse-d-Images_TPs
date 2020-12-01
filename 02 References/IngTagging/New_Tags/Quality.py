# Detect image sharpness and brightness

# Importing packages
import cv2
import matplotlib.pyplot as plt


# image sharpness recognition
def getImageVar(imgPath):

    global sharpness
    sharpness = []
    image = cv2.imread(imgPath)

    # Convert to grayscale image
    img2gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    # Laplacian operator - edge detection
    imageVar = cv2.Laplacian(img2gray,cv2.CV_64F).var() # var(): Calculate variance

    return imageVar


# image sharpnesss recognition
def getSharpness(imageVar):
    if imageVar <= 50:
        sharpness.append("fuzzy")

    return sharpness


# image brightness recognition
# get dark pixels in grayscale image
def getBlackPiex(img_path):
    global darkness
    darkness = []
    img = cv2.imread(img_path, 1)

    # Convert to grayscale image
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Get the number of rows and columns of the grayscale matrix
    r,c = gray_img.shape[:2]
    piexs_sum = r*c # total number of pixels

    # Get dark pixels in grayscale image
    dark_points = (gray_img < 50)   # The artificially setting hyperparameter points that the gray value of 0 ~ 49 is dark
    target_array = gray_img[dark_points]
    dark_sum = target_array.size    # the number of dark pixels
    dark_prop = dark_sum / piexs_sum    # dark pixels ratio

    # Uncomment the line below and show the grayscale histogram
    # hist(img_path)

    if dark_prop >= 0.55:
        darkness.append("dark")
    elif dark_prop <= 0.1:
        darkness.append("light")

    return darkness


# image brightness recognition
# create the grayscale histogram of image
def hist(img_path):
    img = cv2.imread(img_path,1)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    plt.plot(hist)
    plt.subplot(121)
    plt.imshow(img,'gray')
    plt.xticks([])
    plt.yticks([])
    plt.title("Original")
    plt.subplot(122)
    plt.hist(img.ravel(),256,[0,256])
    plt.show()