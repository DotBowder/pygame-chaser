import os
import sys
import pygame
import random
import cv2
from pygame.locals import *
import numpy as np
import keras
from keras.layers.core import *
from keras.layers import *
from keras.utils import *
from keras.optimizers import *
from keras.models import *



#Initialize Variables
WHITE = 255,255,255
GREY = 128,128,128
BLACK = 0,0,0

canvasSize = (100,100)
inputType = 'player'

hasNeuralNetCompletedProcesssing = 0
# Nerual Network will toggle this variable to 1 to let us know to continue
# drawing the frame and then conttinue to the next.

################
# Canvas Class #
################
class Canvas():
	X = int
	y = int

	def __init__(self,size):
		global canvas

		self.W = size[0]
		self.H = size[1]
		canvas = pygame.display.set_mode(size)

################
# Player Class #
################
# The Player Class has position variables for easily determining the player
#location.
#
# Variables:
# W = width, H = height, X = Upper Left Corner X Val, Y = Upper Left Corner
# Y Val
# Center = Pixel (X,Y) in center of player sprite.
# Rect = Rectangle defining player sprite draw bounds on canvas.
# Speed = Distance to move sprite accross canvas per frame. Set to 1/100
# of the canvas size.
#
# Functions:
# UpdateRect() updates the player sprite rectangle. This does NOT draw the
#canvas sprite.
# Move() updates the player sprite location.
# Draw() draws the player sprite location to the canvas.
#
################

class Player():
	W = canvasSize[0]/10 				#Default 1/10 of screen size
	H = canvasSize[1]/10 				#Default 1/10 of screen size
	X = (canvasSize[0]/2) - (W/2) 		#Default to center of screen
	Y = (canvasSize[1]/2) - (H/2) 		#Default to center of screen
	Center = (X - W/2),(Y - H/2)
	Rect = (int,int,int,int)			#Placeholder for later definition
	Speed = canvasSize[0]/100
	Score = 0

	def UpdateRect(self):
		self.Rect = pygame.Rect(self.X,self.Y,self.W,self.H)

	def Move(self,direction):
		if direction == 'up':
			if self.Y > 0:
				self.Y = self.Y - self.Speed
		if direction == 'down':
			if self.Y < canvasSize[1] - self.H:
				self.Y = self.Y + self.Speed
		if direction == 'left':
			if self.X > 0:
				self.X = self.X - self.Speed
		if direction == 'right':
			if self.X < canvasSize[0] - self.W:
				self.X = self.X + self.Speed
		if direction == 'none':
			pass

		self.Center = (self.X - self.W/2),(self.Y - self.H/2)

	def Draw(self):
		self.UpdateRect()
		pygame.draw.rect(canvas, WHITE, self.Rect, 0)

	def AddScore(self,ammount):
		self.Score = self.Score + ammount


################
# Reward Class #
################

class Reward():
	W = canvasSize[0]/10
	H = canvasSize[1]/10
	X = random.randint(0,canvasSize[0]-W)
	Y = random.randint(0,canvasSize[1]-H)
	Center = (X - W/2),(Y - H/2)
	Rect = (int,int,int,int)
	#Speed = canvasSize[0]/100 #May later be used to move rewards on the canvas.

	def UpdateRect(self):
		self.Rect = pygame.Rect(self.X,self.Y,self.W,self.H)

	def Draw(self):
		self.UpdateRect()
		pygame.draw.rect(canvas, BLACK, self.Rect, 0)

	def Respawn(self):
		self.X = random.randint(0,canvasSize[0]-self.W)
		self.Y = random.randint(0,canvasSize[1]-self.H)



##################
# Keyboard Class #
##################

class Keyboard():
	spaceLast = False

	def Update(self, action = 'none'):
		global inputType
		pygame.event.get()
		self.keys = pygame.key.get_pressed()
		if self.keys[K_SPACE] and self.spaceLast == 0:
			if inputType == 'player':
				inputType = 'nn'
				print 'Control Mode: Neural Network'
			elif inputType == 'nn':
				inputType = 'player'
				print 'Control Mode: Player'
		self.spaceLast = self.keys[K_SPACE]
		if inputType == 'player':
			if self.keys[K_UP]:
				return 'up'
			elif self.keys[K_RIGHT]:
				return 'right'
			elif self.keys[K_DOWN]:
				return 'down'
			elif self.keys[K_LEFT]:
				return 'left'
			else:
				return 'none'
		elif inputType == 'nn':
			return action


def Collision(Rect1, Rect2):
	return pygame.Rect.colliderect(Rect1, Rect2)

def UpdateScreen():
	pygame.display.update()
	pygame.time.delay(16)

def GetFrame():
	multichannelframe = pygame.surfarray.array3d(pygame.display.get_surface())
	frame = cv2.cvtColor(cv2.resize(multichannelframe, (canvasSize[0], canvasSize[1])), cv2.COLOR_BGR2GRAY)
	return frame


def TrueDirection(player, reward):
	xDif = player.X - reward.X
	yDif = player.Y - reward.Y

	if abs(xDif) > abs(yDif): 		# If the player X is further from the reward
		if xDif < 0: 				# The right way to go is Left or Right
			return np.array([0],[0],[0],[1])
		elif xDif < 0:
			return np.array([0],[1],[0],[0])
	elif abs(xDif) <= abs(yDif):	# If the player Y is further from the reward
		if yDif < 0:				# The right way to go is Up or Down
			return np.array([0],[0],[1],[0])
		elif yDif >= 0:
			return np.array([1],[0],[0],[0])




# load json and create model
json_file = open('chaser-model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
# load weights into new model
model.load_weights("chaser-model.h5")
print("\nLoaded model from disk\n")

def TestNN():
	frame = GetFrame()
	frame = np.reshape(frame,(1,100,100,1))
	prediction = model.predict(frame, batch_size=1, verbose=0)
	#print prediction.shape
	print prediction
	if abs(prediction[0][0]) > 0.9:
		return 'up'
	elif abs(prediction[0][1]) > 0.9:
		return 'right'
	elif abs(prediction[0][2]) > 0.9:
		return 'down'
	elif abs(prediction[0][3]) > 0.9:
		return 'left'





#Create Display
screen = Canvas(canvasSize)
keyboard = Keyboard()

#Create Player
player = Player()
reward = Reward()

#Draw initial screen elements
canvas.fill(GREY)
player.Draw()
reward.Draw()

action = TestNN()

while True:
	#currentFrame = GetFrame()
	#reshapedFrame = np.reshape(currentFrame,(1,200,200,3))
	#print type(currentFrame)
	#nn.Train(reshapedFrame,TrueDirection(player,reward))

	canvas.fill(GREY)
	keyboard.Update()
	if inputType == 'player':
		player.Move(keyboard.Update())
	elif inputType == 'nn':
		player.Move(action)
	if Collision(player.Rect,reward.Rect):
		reward.Respawn()
		player.AddScore(10)
		print player.Score
	player.Draw()
	reward.Draw()
	action = TestNN()
	#print GetFrame()

	UpdateScreen()
