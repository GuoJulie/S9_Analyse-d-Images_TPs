# Detect main elements
# Mask_Rcnn - Tensorflow pre-trained model by the dataset MSCOCO


# Importing packages
import cv2 as cv
import numpy as np
import os.path
import sys
import random
import tarfile


def initial(folder_path):
    global classes, new_classes, new_classId, confThreshold, maskThreshold, colors, net

    # Initialize the parameters
    confThreshold = 0.5  # Confidence threshold
    maskThreshold = 0.3  # Mask threshold

    # Give the textGraph and weight files for the model
    tar_path = folder_path + '/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz'
    model_path = folder_path + '/mask_rcnn_inception_v2_coco_2018_01_28'
    if not os.path.exists(model_path) or not os.listdir(model_path): # if the folder does not exist or it is empty, unzip it
        un_tar(tar_path)

    textGraph = folder_path + '/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt'
    modelWeights = model_path + '/frozen_inference_graph.pb'

    # Load the network
    net = cv.dnn.readNetFromTensorflow(modelWeights, textGraph)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    # Load names of classes and define new classes as needed
    classesFile = folder_path + '/mscoco_labels.names'
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    new_classes = ['human', 'byke', 'car', 'plane', 'van', 'animal']
    new_classId = [0, 1, 2, 4, 7, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    # Load the classes
    colors = []  # [0,0,0]
    colorsFile = folder_path + '/colors.txt'
    with open(colorsFile, 'rt') as f:
        colorsStr = f.read().rstrip('\n').split('\n')
    for i in range(len(colorsStr)):
        rgb = colorsStr[i].split(' ')
        color = np.array([float(rgb[0]), float(rgb[1]), float(rgb[2])])
        colors.append(color)


# untar files
def un_tar(file_name):
    folder_path = os.path.dirname(file_name)
    tar = tarfile.open(file_name)
    names = tar.getnames()
    for name in names:
        tar.extract(name, folder_path) # Create a directory with the same name
    tar.close()


# Draw the predicted bounding box, colorize and show the mask on the image
def drawBox(img, classId, conf, left, top, right, bottom, classMask):

    # Draw a bounding box.
    cv.rectangle(img, (left, top), (right, bottom), (255, 178, 50), 3)

    # Print a label of class.
    label = '%.2f' % conf
    if classId in new_classId:
        if classId > 14 and classId < 25:
            result_ME.append(new_classes[5])
            label = '%s:%s' % (new_classes[5], label)
        else:
            result_ME.append(new_classes[new_classId.index(classId)])
            label = '%s:%s' % (new_classes[new_classId.index(classId)], label)
    else:
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(img, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(img, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    # Resize the mask, threshold, color and apply it on the image
    classMask = cv.resize(classMask, (right - left + 1, bottom - top + 1))
    mask = (classMask > maskThreshold)
    roi = img[top:bottom + 1, left:right + 1][mask]

    colorIndex = random.randint(0, len(colors)-1)
    color = colors[colorIndex]

    img[top:bottom + 1, left:right + 1][mask] = ([0.3 * color[0], 0.3 * color[1], 0.3 * color[2]] + 0.7 * roi).astype(
        np.uint8)

    # Draw the contours on the image
    mask = mask.astype(np.uint8)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img[top:bottom + 1, left:right + 1], contours, -1, color, 3, cv.LINE_8, hierarchy, 100)


# For each img, extract the bounding box and mask for each detected object
def postprocess(boxes, masks, img):
    # Output size of masks is NxCxHxW where
    # N - number of detected boxes
    # C - number of classes (excluding background)
    # HxW - segmentation shape

    global nb_classId, nb_classId_deduplicate
    nb_classId = []
    nb_classId_deduplicate = []

    numClasses = masks.shape[1]
    numDetections = boxes.shape[2]

    imgH = img.shape[0]
    imgW = img.shape[1]

    for i in range(numDetections):
        box = boxes[0, 0, i]
        mask = masks[i]
        score = box[2]

        if score > confThreshold:
            classId = int(box[1])
            nb_classId.append(classId)

            # Extract the bounding box
            left = int(imgW * box[3])
            top = int(imgH * box[4])
            right = int(imgW * box[5])
            bottom = int(imgH * box[6])

            left = max(0, min(left, imgW - 1))
            top = max(0, min(top, imgH - 1))
            right = max(0, min(right, imgW - 1))
            bottom = max(0, min(bottom, imgH - 1))

            # Extract the mask for the object
            classMask = mask[classId]

            # Draw bounding box, colorize and show the mask on the image
            drawBox(img, classId, score, left, top, right, bottom, classMask)

            nb_classId_deduplicate = list(set(nb_classId))


def test_ME(image_path, folder_path):

    global result_ME
    result_ME = []

    # initialize
    initial(folder_path)

    # Open the image file
    if not os.path.isfile(image_path):
        print("Input image file ", image_path, " doesn't exist")
        sys.exit(1)
    img = cv.imread(image_path)

    # Create a 4D blob from a img.
    blob = cv.dnn.blobFromImage(img, swapRB=True, crop=False)

    # Set the input to the network
    net.setInput(blob)

    # Run the forward pass to get output from the output layers
    boxes, masks = net.forward(['detection_out_final', 'detection_masks'])

    # Extract the bounding box and mask for each of the detected objects
    postprocess(boxes, masks, img)

    # Uncomment these lines below to generate and show the img with the detection boxes and masks
    # # Put efficiency information.
    # t, _ = net.getPerfProfile()
    # label = 'Mask-RCNN on 2.5 GHz Intel Core i7 CPU, Inference time for a img : %0.0f ms' % abs(t * 1000.0 / cv.getTickFrequency())
    # cv.putText(img, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    # # Write the new image
    # if (image_path):
    #     outputFile = image_path[:-4] + '_mask_rcnn_out_py.jpg'
    #     cv.imwrite(outputFile, img.astype(np.uint8))
    # img = cv.imread(outputFile)
    # cv.imshow("OutputFile", img)

    result = list(set(result_ME))
    return result



