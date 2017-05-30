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







#Initialize Colors
WHITE = 255,255,255
GREY = 128,128,128
BLACK = 0,0,0

#Initialize Pygame Canvas
canvasSize = (100,100)
canvas = pygame.display.set_mode(canvasSize)

#Define Game Objects
class Player():
    W = canvasSize[0]/10 				#Default 1/10 of screen size
    H = canvasSize[1]/10 				#Default 1/10 of screen size
    X = (canvasSize[0]/2) - (W/2) 		#Default to center of screen
    Y = (canvasSize[1]/2) - (H/2) 		#Default to center of screen
    Rect = (int,int,int,int)			#Placeholder for later definition

    def RandomRect(self):
        self.X = random.randint(0,canvasSize[0]-self.W)
        self.Y = random.randint(0,canvasSize[1]-self.H)
        self.Rect = pygame.Rect(self.X,self.Y,self.W,self.H)

    def Draw(self):
        pygame.draw.rect(canvas,  WHITE, self.Rect, 0)

class Reward():
    W = canvasSize[0]/10
    H = canvasSize[1]/10
    X = random.randint(0,canvasSize[0]-W)
    Y = random.randint(0,canvasSize[1]-H)
    Rect = (int,int,int,int)

    def RandomRect(self):
        self.X = random.randint(0,canvasSize[0]-self.W)
        self.Y = random.randint(0,canvasSize[1]-self.H)
        self.Rect = pygame.Rect(self.X,self.Y,self.W,self.H)

    def Draw(self):
        pygame.draw.rect(canvas, BLACK, self.Rect, 0)

#Define Object Manipulation Methods/Functions
def GetClosestPathDir(player,reward):
    xDif = player.X - reward.X
    yDif  = player.Y - reward.Y
    abs_xDif = abs(xDif)
    abs_yDif = abs(yDif)
    #print 'Player X difference: \t', abs_xDif, '\tPlayer Y difference: \t', abs_yDif
    up = 0
    right = 1
    down = 2
    left = 3

    if abs_xDif > abs_yDif:
        # If there is a greater distance between the player and the reward on the X axis than the Y axis,
        # then the player will need to move left or right before continuing.
        if xDif > 0:
            # If the difference between the player's X val and the reward's X val is positive,
            # then the player is further right than the reward, and the player needs to move left.
            return left
        if xDif < 0:
            # If the difference between the player's X val and the reward's X val is negative,
            # then the player is further left than the reward, and the player needs to move right.
            return right
    elif abs_xDif <= abs_yDif:
        # If there is a greater distance between the player and the reward on the Y axis than the X axis,
        # then the player will neeed to move up or down before continuing.
        if yDif > 0:
            # If the difference between the player's Y val and the reward's Y val is positive,
            # then the player is furhter down than the reward, and the player needs to move up.
            return up
        elif yDif < 0:
            # If the difference between the player's Y val and the reward's Y val is negavtive,
            # then the player is further up than the reward, and the player needs to move down.
            return down

def GenerateTrainingFrames(numberOfIterations):
    iterationCounter = 0
    multichannelframe = np.zeros((canvasSize[0],canvasSize[1],3),dtype=int)
    frame = np.zeros((canvasSize[0],canvasSize[1]),dtype=int)

    # x_train contains the images in int format
    # image  x  200px  x  200px  x  3 color channel
    x_train = np.zeros((numberOfIterations,canvasSize[0],canvasSize[1]),dtype=int)
    # y_train contains the preferred direction as an int
    # image  x  correct direction
    y_train = np.zeros((numberOfIterations,1),dtype=int)

    # Start Print to Console
    # If using too much pixel-data, the amount of memory allocated can
    # very quickly spiral out of control.
    print 'Memory Allocation for X:\t',x_train.nbytes/1000/1000,'MB'
    print 'Memory Allocation for Y:\t',y_train.nbytes/1000/1000,'MB'
    # End Print to Console

    while iterationCounter < numberOfIterations:
        #Create Player and Reward
        player = Player()
        reward = Reward()
        #Generate Random Rectangles for both the player and the reward
        player.RandomRect()
        reward.RandomRect()
        #Determine best move choice based on shortest-path
        optimalDirection = GetClosestPathDir(player,reward)

        # If the player and the reward are not overlapping
        if pygame.Rect.colliderect(player.Rect, reward.Rect) == 0:
            # Draw to screen.
            canvas.fill(GREY)
            player.Draw()
            reward.Draw()
            pygame.display.update()

            # Pull frame from current canvas in multichannel RGB format
            # (256,256,256) (R,G,B)
            multichannelframe = pygame.surfarray.array3d(pygame.display.get_surface())

            # Convert multichannel frame into single channel frame
            # RGB -> Greyscale     (256,256,256) -> (256)
            frame = cv2.cvtColor(cv2.resize(multichannelframe, (canvasSize[0], canvasSize[1])), cv2.COLOR_BGR2GRAY)

            # Dump frame data into x_train[currentImage]
            np.copyto(x_train[iterationCounter],frame)
            # Dump label/Direction data into y_train[currentImage]
            y_train[iterationCounter] = optimalDirection

            # Start Print to Console
            #optimalDirectionString = ''
            #if optimalDirection == 0:
            #    optimalDirectionString = 'up'
            #elif optimalDirection == 1:
            #    optimalDirectionString = 'right'
            #elif optimalDirection == 2:
            #    optimalDirectionString = 'down'
            #elif optimalDirection == 3:
            #    optimalDirectionString = 'left'

            #print 'Frame: \t', iterationCounter, '\tOptimalDir: \t', optimalDirectionString
            #print 'Frames to Generate: \t', numberOfIterations
            # End Print to Console

            iterationCounter = iterationCounter + 1

            # To slow down the frame generation process, uncomment time delay.
            #pygame.time.delay(5000)
        else:
            # If the player and the reward are overlapping don't do anything
            # We'll return to while loop on the same iteration step.
            pass
    return x_train,y_train


#x_train,y_train = GenerateTrainingFrames(20000)






# Part 2
# Process Data Through Neural Network




nb_classes = 4

#Assign Input Variables
numberOfEpochs = 1
batch_size = 100

trainingFrameCount = 50000
testingFrameCount = 10000

layer1_size = 100
layer2_size = 100
layer3_size = 100
#layer3_size = int(sys.argv[5])

X_train, y_train = GenerateTrainingFrames(trainingFrameCount)
X_test, y_test = GenerateTrainingFrames(testingFrameCount)
#print X_train.shape, X_test.shape

X_train = np.reshape(X_train,(trainingFrameCount,100,100,1))
X_test = np.reshape(X_test,(testingFrameCount,100,100,1))

#X_train = X_train.reshape(trainingFrameCount,10000)
#X_test = X_test.reshape(testingFrameCount,10000)


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

print X_train.shape, ' '

print(X_train.shape[0],'train samples')
print(X_test.shape[0],'train samples')


Y_train = np_utils.to_categorical(y_train,nb_classes)
Y_test = np_utils.to_categorical(y_test,nb_classes)

if True:
    # load json and create model
    json_file = open('chaser-model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    # load weights into new model
    model.load_weights("chaser-model.h5")
    print("\nLoaded model from disk\n")
    #model.predict(self, x, batch_size=32, verbose=0)
else:
    model = Sequential()
    model.add(keras.layers.convolutional.Conv2D(layer1_size, 10, input_shape=(100,100,1)))
    model.add(Activation('relu'))
    model.add(keras.layers.pooling.MaxPooling2D(pool_size=(10,10)))

    model.add(keras.layers.convolutional.Conv2D(layer2_size, 4))
    model.add(Activation('relu'))
    model.add(keras.layers.pooling.MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(layer3_size))
    model.add(Activation('relu'))
    model.add(Dropout(0.01))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer = RMSprop(),
              metrics=['accuracy'])

history = model.fit(X_train,Y_train,
                batch_size = batch_size,
                nb_epoch = numberOfEpochs,
                verbose = 1,
                validation_data = [X_test,Y_test])

score = model.evaluate(X_test, Y_test,verbose=1)

print '\nTest Score:',score[0]
print('Test Accuracy:',score[1])

# serialize model to JSON
model_json = model.to_json()
with open("chaser-model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("chaser-model.h5")
print("Saved model to disk")
