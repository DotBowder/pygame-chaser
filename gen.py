from keras.layers.core import *
from keras.layers import *
from keras.utils import *
from keras.optimizers import *
from keras.models import *
import numpy as np
import keras
import cv2
import pygame
import random
import sys


if raw_input('Are you sure you want to overwrite your existing model? (y/n)') == 'y':
    pass
else:
    exit()


##############################
## Define  Hyper Parameters ##
##############################
trainingFrameCount = 4000
testingFrameCount = 4000

layer1_size = 40
layer2_size = 100
layer3_size = 120
layer4_size = 128
layer5_size = 48
layer6_size = 48
layer7_size = 48
layer8_size = 32
nb_classes = 4

###################
##  Define Model ##
###################
model = Sequential()
model.add(keras.layers.convolutional.Conv2D(layer1_size, 15, strides=2, input_shape=(100,100,1)))
model.add(Activation('relu'))
model.add(keras.layers.pooling.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.convolutional.Conv2D(layer2_size, 5))
model.add(Activation('relu'))
model.add(keras.layers.pooling.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.convolutional.Conv2D(layer3_size, 2))
model.add(Activation('relu'))
model.add(keras.layers.pooling.MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
#model.add(Dense(layer3_size))
#model.add(Activation('relu'))
#model.add(Dropout(0.1))
model.add(Dense(layer4_size))
model.add(Activation('relu'))
model.add(Dropout(0.5))
#model.add(Dense(layer5_size))
#model.add(Activation('relu'))
#model.add(Dropout(0.05))
#model.add(Dense(layer6_size))
#model.add(Activation('relu'))
#model.add(Dropout(0.05))
model.add(Dense(layer7_size))
model.add(Activation('relu'))
model.add(Dropout(0.01))
model.add(Dense(layer8_size))
model.add(Activation('relu'))
model.add(Dropout(0.01))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.summary()


###########################
## Save TensorBoard Data ##
###########################
tensorBoardCallback = keras.callbacks.TensorBoard(log_dir='/your-home-dir/chaser/model/logs', histogram_freq=0, write_graph=False, write_images=True)


########################
## Save Model to DIsk ##
########################
jsonModel = model.to_json()
with open("chaser-model.json", "w") as jsonFile:
    jsonFile.write(jsonModel)
model.save_weights("chaser-model.h5")
print("Saved model to disk")
