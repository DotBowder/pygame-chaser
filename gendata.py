import numpy as np
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
        if xDif <= 0:
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
        elif yDif <= 0:
            # If the difference between the player's Y val and the reward's Y val is negavtive,
            # then the player is further up than the reward, and the player needs to move down.
            return down

def GenerateTrainingFrames(numberOfIterations):
    iterationCounter = 0
    canvas = pygame.display.set_mode(canvasSize)
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
        #if pygame.Rect.colliderect(player.Rect, reward.Rect) == 0:
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


        iterationCounter = iterationCounter + 1

        # To slow down the frame generation process, uncomment time delay.
        #pygame.time.delay(5000)
    return x_train,y_train

for dataset in range(5):
    x,y = GenerateTrainingFrames(100000)
    xdir = '/your-home-dir/chaser/data/'+str(dataset)+'_x.npy'
    ydir = '/your-home-dir/chaser/data/'+str(dataset)+'_y.npy'
    np.save(xdir, x)
    np.save(ydir, y)
