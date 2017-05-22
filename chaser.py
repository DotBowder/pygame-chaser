import os
import sys
import pygame
import random
from pygame.locals import *
from math import pi


# Static Vars
WHITE = 255,255,255
BLACK = 0,0,0
up, right, down, left = 0, 1, 2, 3

# Function for generating a new reward sprite
def rewardGen():
	newX = random.randint(0, windowSize[0]-rewardSize[0])
	newY = random.randint(0, windowSize[1]-rewardSize[1])
	return (newX,newY)



############
### Init ###
############
#
# Init functions to get our declarations and setup out of the way.
#

def InitCreateWindow():
	global windowSize
	global window
	
	windowSize = 200,200
	window = pygame.display.set_mode(windowSize)
	
	# We need a window to use for pygame

def InitDrawPlayer(playersize):
	global playerScore
	global playerMov
	global playerSpeed
	global playerSize
	global playerPos
	global playerRect
	global playerTotalMoves
	
	playerTotalMoves = 0
	playerScore = 0
	playerMov = random.randint(0,3)
	playerSpeed = 1
	playerSize = [playersize,playersize]
	playerPos = [windowSize[0]/2,windowSize[1]/2]
	playerRect = pygame.Rect(playerPos[0],playerPos[1],playerSize[0],playerSize[1])
	
	# Declare player variables

def InitDrawReward():
	global rewardCount
	global rewardValue
	global rewardSize
	global rewardPos
	global rewardRect
		
	rewardCount = 0
	rewardValue = 10
	rewardSize = playerSize
	rewardPos = rewardGen()
	rewardRect = pygame.Rect(rewardPos[0],rewardPos[1],rewardSize[0],rewardSize[1])
	
	# Declare reward variables

def InitPlayerDist():
	global playerDist
	
	playerDist = LivePlayerDist()
	
	# Declare player's initial distance from reward sprite

def InitProcessInputs():
	global reqMov
	
	reqMov = playerMov
	
	# Declare the requested move variable so that it can be used later



############
### Live ###
############
#
# Live functions will be stepped through, to generate the game frame by frame.
#

def LiveDrawPlayer():
	global playerRect
	playerRect = pygame.Rect(playerPos[0],playerPos[1],playerSize[0],playerSize[1])
	player = pygame.draw.rect(window, WHITE, playerRect, 0)
	
	# Use the player variables to draw a player Rectangle


def LiveDrawReward():
	global rewardRect
	rewardRect = pygame.Rect(rewardPos[0],rewardPos[1],rewardSize[0],rewardSize[1])
	reward = pygame.draw.rect(window, WHITE, rewardRect, 0)
	
	# Use the reward variables to draw a reward rectangle

def LiveProcessInputs():
	global playerMov
	global reqMov
	pygame.event.get()					
	keys = pygame.key.get_pressed()
	if keys[K_UP] and playerMov != down:
		reqMov = up
	elif keys[K_RIGHT] and playerMov != left:
		reqMov = right
	elif keys[K_DOWN] and playerMov != up:
		reqMov = down
	elif keys[K_LEFT] and playerMov != right:
		reqMov = left
	else:
		reqMov = playerMov
	playerMov = reqMov
	
	# Pull keypress data and check if up,right,down,or left is pressed. If so, check if the direction is eligible and change playerMov to the new direction.

def LiveMovePlayer():
	global playerMov
	global playerPos
	global playerSpeed
	global playerTotalMoves
	
	if playerMov == up and (playerPos[1] - playerSpeed) > 0:
		playerPos[1] = playerPos[1] - playerSpeed
	elif playerMov == right and (playerPos[0] + playerSpeed + playerSize[0]) < windowSize[0]:
		playerPos[0] = playerPos[0] + playerSpeed
	elif playerMov == down and (playerPos[1] + playerSpeed + playerSize[1]) < windowSize[1]:
		playerPos[1] = playerPos[1] + playerSpeed
	elif playerMov == left and (playerPos[0] - playerSpeed) > 0:
		playerPos[0] = playerPos[0] - playerSpeed
	else:
		pass
	playerTotalMoves = playerTotalMoves + 1
	
	# Update player position based on playerMov variable.
	# playerMov reports the direction of the player.
	# 0 is up, 1 is right, 2 is down, 3 is left
	# playerSpeed is the variable that tells us how many pixels we want to jump. 
	# This can be useful for speeding up the game, however, it would be unwize to set the playerSpeed
	# to a bigger number than playerSize + rewardSize as that would create gaps where the player
	# could hop right over the reward.

def LiveAssessReward():
	global rewardPos
	global playerScore
	global playerRect
	global rewardRect
	global playerDist
	global playerTotalMoves
	global playerExcessMoves
	
	collisionStatus = pygame.Rect.colliderect(playerRect, rewardRect)
	if collisionStatus == True:
		playerScore = playerScore + rewardValue
		playerExcessMoves = playerTotalMoves - playerDist
		if playerExcessMoves < 0:
			playerExcessMoves = 0
		print 'Player Score:',playerScore,'\tPrev PlayerDist:',playerDist,'\tExcess Moves:',playerExcessMoves,'\tTotal Moves:',playerTotalMoves
		rewardPos = rewardGen()
		playerDist = LivePlayerDist()
		playerTotalMoves = 0
	else:
		pass
	
	# LiveAssessReward determines if the playerRect and the rewardRect are colliding.
	# If they collide, then we need to + the playerScore, calculate the excess moves used by the player,
	# generate a new reward sprite by randomly generating new X,Y coords, and reset the player movecount.

def LiveExportWindow():
	image_data = pygame.surfarray.array3d(pygame.display.get_surface())
	return image_data
	
	# This is used to return a 3d array of the pixels on the screen.
	# This will be used as input for a Machine Learning neural network.

def LivePlayerDist():
	global playerDist
	
	dist = abs(playerPos[0]-rewardPos[0]) + abs(playerPos[1]-rewardPos[1])
	dist = dist / playerSpeed
	return dist
	
	# This function calculates the minimum physical moves that the player could take to reach the reward sprite. (Doesn't account for sprite size and is tied to upper left corner coords of each sprite.)


###
# Class
###
#
# The class wraps up all of our functions into one nice little container allowing this to be called in another python script.
# More passthrough variables will be added at a later time.
#

class Game:
	def __init__(self,playersize):
		# Run Init
		InitCreateWindow()
		InitDrawPlayer(playersize)
		InitDrawReward()
		InitPlayerDist()
		InitProcessInputs()
		
	def Draw(self):
		# Run Live
		window.fill(BLACK)			# Wipe Screen
		LiveDrawPlayer()			# Draw Player
		LiveDrawReward()			# Draw Reward
		LivePlayerDist()			# Get Player Distance from Reward
		

	def Process(self, action = (0,0,0,0)):
		LiveProcessInputs()			# Did the user press a key? If so, update playerMov Direction (Will eventually be replaced with an action variable passed through by neural network at a later time.)
		LiveMovePlayer()			# Move Player toward playerMov Direction
		LiveAssessReward()			# Did the player collide with the Reward?
		pygame.display.update() 	# Refresh the display.
		pygame.time.delay(4)		# Wait X ms 

	def GetFrame(self):
		LiveExportWindow()			# Returns a 3d array of pixel data.



# Create class object and run
game = Game(10)
while 1:
	game.Draw()
	game.GetFrame()
	game.Process()


