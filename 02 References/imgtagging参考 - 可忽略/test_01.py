import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

import cv2

import os

def training():
    folder = "./Tagging/"
    classification = ["yellow", "green", "red", "blue", "brown", "gray", "white", "black", "orange",
                      "inside", "outside", "nature", "city",
                      "human", "face", "animal", "car", "plane", "van", "byke",
                      "sky", "sun", "house", "tree", "water", "sea", "mountain", "snow", 'ski',
                      "fuzzy", "sharp", "dark", "light",
                      "solated", "multiple"]

    x_set = []
    y_set = []

    for file in os.listdir(folder):
        if file != "GT":
            x_set.append(cv2.imread(folder + file))

            labels = open(folder + "GT/" + file.split('.')[0] + ".txt").read()
            labels = labels.split(',')
            for i in range(len(labels)):
                labels[i] = classification.index(labels[i].replace(" ", ""))
                print(folder + "GT/" + file.split('.')[0] + ".txt")

            y_set.append(labels[0])


    print("x_set:", len(x_set))
    print("y_set:", len(y_set))

    x_train = np.array(x_set)


    y_train = np.array(y_set)
    y_train_one_hot = to_categorical(y_train)

    x_train = x_train/255

    model = Sequential()
    model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(32, 32, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(500, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(250, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])



    hist = model.fit(x_train, y_train_one_hot,
                     batch_size=256, epochs=10, validation_split=0.2)


if __name__ == '__main__':
    print('Hello')
    training()