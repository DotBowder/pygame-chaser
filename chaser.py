import os
import sys
import pygame
import random
from pygame.locals import *

#Initialize Variables
WHITE = 255,255,255
GREY = 128,128,128
BLACK = 0,0,0

canvasSize = (100,100)

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
# The Player Class has position variables for easily determining the player location.
#
# Variables:
# W = width, H = height, X = Upper Left Corner X Val, Y = Upper Left Corner Y Val
# Center = Pixel (X,Y) in center of player sprite.
# Rect = Rectangle defining player sprite draw bounds on canvas.
# Speed = Distance to move sprite accross canvas per frame. Set to 1/100 of the canvas size.
# 
# Functions:
# UpdateRect() updates the player sprite rectangle. This does NOT draw the canvas sprite.
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
		self.Center = (self.X - self.W/2),(self.Y - self.H/2)
		
	def Draw(self):
		self.UpdateRect()
		pygame.draw.rect(canvas, WHITE, self.Rect, 0)


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



##################
# Keyboard Class #
##################

class Keyboard():	
	def Update(self):
		pygame.event.get()
		self.keys = pygame.key.get_pressed()
		if self.keys[K_UP]:
			return 'up'
		elif self.keys[K_RIGHT]:
			return 'right'
		elif self.keys[K_DOWN]:
			return 'down'
		elif self.keys[K_LEFT]:
			return 'left'
		else:
			return 4



def UpdateScreen():
	pygame.display.update() 
	pygame.time.delay(16)



screen = Canvas(canvasSize)
canvas.fill(GREY)
keyboard = Keyboard()

player = Player()
reward = Reward()


player.Draw()
reward.Draw()

for iteration in range(2000):
	canvas.fill(GREY)	
	player.Move(keyboard.Update())
	player.Draw()
	reward.Draw()
	UpdateScreen()

#pygame.time.delay(2000)
