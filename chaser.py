import os
import sys
import pygame
from pygame.locals import *
from math import pi
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)

RED = (255, 0, 0)
RED_DIM = (192, 0, 0)

YELLOW = (255, 255, 0)

GREEN = (0, 255, 0)
GREEN_DIM = (0, 192, 0)

TEAL = (0, 255, 255)

BLUE = (0, 0, 255)
BLUE_DIM = (0, 0, 192)

diag_mode = True

# Se player difficulty
difficulty = {}
difficulty['easy'] = {'p_speed': 2, 'e_speed': 1,
                      'e_max_size': 30, 'e_growth_rate': 0.01, 'num_enemies': 2, 'num_rewards': 2}
difficulty['medium'] = {'p_speed': 3, 'e_speed': 2,
                        'e_max_size': 40, 'e_growth_rate': 0.05, 'num_enemies': 3, 'num_rewards': 2}
difficulty['hard'] = {'p_speed': 4, 'e_speed': 2,
                      'e_max_size': 60, 'e_growth_rate': 0.08, 'num_enemies': 5, 'num_rewards': 2}
difficulty['insane'] = {'p_speed': 4, 'e_speed': 3,
                        'e_max_size': 100, 'e_growth_rate': 0.10, 'num_enemies': 7, 'num_rewards': 2}
player_difficulty = 'easy'



# Define screen size here
window_size = window_width, window_height = 600, 400
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Chaser")
pygame.init()
pygame_events = pygame.event.get()
monospace_font = pygame.font.SysFont("monospace", 15)
clock = pygame.time.Clock()
control_mode = 'player'

# Player Rectangle
size = (10, 10)
x, y = random.randint(
    0, (window_width - size[0])), random.randint(0, (window_height - size[1]))
p_center = x + (size[0] / 2), y + (size[1] / 2)
p_rect = pygame.Rect(x, y, size[0], size[1])
p_color = BLUE
p_score = 0
p_speed = difficulty[player_difficulty]['p_speed']
every_10_cycles = 0

# Define Rewards List for keeping track of all of our Rewards
rewards = {}
r_color = GREEN

# Define Enemies List for keeping track of all of our Enemies
enemies = {}
e_color = RED

held_keys = {}
held_keys['Up'] = False
held_keys['Down'] = False
held_keys['Left'] = False
held_keys['Right'] = False
# Buttons Defined
b = {}
b_size = (150, 50)
# (Button Rectangle, Button Standard Color, Button Hovor Color, Hover Status)
b[0] = (pygame.Rect(0, window_size[1] - b_size[1] -
                    10, b_size[0], b_size[1]), RED, RED_DIM, 0)
b[1] = (pygame.Rect(160, window_size[1] - b_size[1] -
                    10, b_size[0], b_size[1]), GREEN, GREEN_DIM, 0)
b[2] = (pygame.Rect(320, window_size[1] - b_size[1] -
                    10, b_size[0], b_size[1]), BLUE, BLUE_DIM, 0)
b[3] = (pygame.Rect(480, window_size[1] - b_size[1] -
                    10, b_size[0], b_size[1]), BLACK, GREY, 0)
b[4] = (pygame.Rect(640, window_size[1] - b_size[1] -
                    10, b_size[0], b_size[1]), WHITE, GREY, 0)
# Buttons get copied to buttons{} after drawing to screen
buttons = {}

# Mouse Location
m_loc = pygame.Rect(0, 0, 10, 10)


diag_core = True

######################################################
# Algarithms
# The Go To Player function finds the closest direction to the Player,
# and moves the input rectangle 1 step closer to the player.
def GoToPlayer(rect, speed, chance):
    if diag_core == True:
        print('\tGoToPlayer:',rect,':',speed,':',chance)
    x, y = RectCenter(rect)
    x_distance = p_center[0] - x
    y_distance = p_center[1] - y

    rand = random.randint(0, 100)
    if rand <= chance:
        if abs(x_distance) > abs(y_distance):
            if x_distance > 0:
                rect = GoRight(rect, dist=speed)
            elif x_distance < 0:
                rect = GoLeft(rect, dist=speed)
        elif abs(y_distance) >= abs(x_distance):
            if y_distance > 0:
                rect = GoDown(rect, dist=speed)
            elif y_distance < 0:
                rect = GoUp(rect, dist=speed)
    return rect

# GrowRect allows you to grow a rectangle based on a random chance
# by setting the chance variable between 0 and 100, you define the
# probability of the growth occuring.
# A chance of 0 has a 0% chance of growth occurance per call.
# A chance of 100 has a 100% chance of trowth occurance per call.
def GrowRect(rect, growth_size, max_size, chance):
    if diag_core == True:
        print('\tGrowRect:',rect,':',growth_size,':',max_size,':',chance)
    rand = random.randint(0, 100)
    if rand <= chance and rect[2] < max_size:
        return (rect[0], rect[1], rect[2] + growth_size, rect[3] + growth_size)
    else:
        return rect
######################################################

######################################################
# Helper Functions
def Collision(rec1, rec2):
    if diag_core == True:
        print('\tCollision:',rec1,':',rec2)
    rec1 = pygame.Rect(rec1)
    rec2 = pygame.Rect(rec2)
    return pygame.Rect.colliderect(rec1, rec2)
def RectCenter(rect):
    Diag('\tRectCenter:'+str(rect))
    return rect[0] + (rect[2] / 2), rect[1] + (rect[3] / 2)
def GetEvents():
    if diag_core == True:
        print('GetEvents')
    global pygame_events
    pygame_events = pygame.event.get()
def WipeScreen():
    if diag_core == True:
        print('WipeScreen')
    screen.fill(BLACK)
def UpdateScreen():
    if diag_core == True:
        print('UpdateScreen')
    pygame.display.update()
def Quit():
    if diag_core == True:
        print('Quit')
    pygame.display.quit()
    sys.exit(0)
def ExitCheck():
    if diag_core == True:
        print('ExitCheck')
    if pygame.key.get_pressed()[K_ESCAPE]:
        Quit()
    if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_c]:
        Quit()
######################################################

######################################################
# Add Elements
def AddEnemy(size=(10, 10)):
    if diag_core == True:
        print('AddEnemy:',size)
    # Generate a new enemy rectangle and add it to the enemies dictionary.
    global enemies
    x, y = random.randint(
        0, (window_width - size[0])), random.randint(0, (window_height - size[1]))
    rect = pygame.Rect(x, y, size[0], size[1])

    counter = 0
    for num, enemy in enemies.items():
        print(num)
        counter += 1
    enemies[counter] = rect

def AddReward(size=(10, 10)):
    if diag_core == True:
        print('AddReward:',size)
    global rewards
    x, y = random.randint(
        0, (window_width - size[0])), random.randint(0, (window_height - size[1]))
    rect = (x, y, size[0], size[1])
    counter = 0
    for num, entry in rewards.items():
        counter = num
    rewards[counter + 1] = rect
######################################################

def Diag(msg):
    if diag_core == True:
        print(msg)

######################################################
# Process Game Inputs
def UpdateMouse(loc):
    Diag('UpdateMouse:'+ str(loc))
    global m_loc
    m_loc = pygame.Rect(loc[0], loc[1], 10, 10)
    MouseCollision()
def ProcessInputs():
    global p_rect
    global every_10_cycles
    if diag_core == True:
        Diag('ProcessInputs')


    if diag_core == True:
        Diag('\tHeldKeyCheck:')
    try:
        if held_keys['Left'] == True:
            Diag('\t\theld_keys["Left"] is True')
            p_rect = GoLeft(p_rect, dist=p_speed, hold=True)
        else:
            Diag('\t\theld_keys["Left"] is False')
    except:
        Diag('\t\theld_keys["Left"] Lookup Failed')

    try:
        if held_keys['Right'] == True:
            Diag('\t\theld_keys["Right"] is True')
            p_rect = GoRight(p_rect, dist=p_speed, hold=True)
        else:
            Diag('\t\theld_keys["Right"] is False')
    except:
        Diag('\t\theld_keys["Right"] Lookup Failed')

    try:
        if held_keys['Down'] == True:
            Diag('\t\theld_keys["Down"] is True')
            p_rect = GoDown(p_rect, dist=p_speed, hold=True)
        else:
            Diag('\t\theld_keys["Down"] is False')
    except:
        Diag('\t\theld_keys["Down"] Lookup Failed')

    try:
        if held_keys['Up'] == True:
            Diag('\t\theld_keys["Up"] is True')
            p_rect = GoUp(p_rect, dist=p_speed, hold=True)
        else:
            Diag('\t\theld_keys["Down"] is False')
    except:
        Diag('\t\theld_keys["Up"] Lookup Failed')


    for entry in pygame_events:
        Diag('\tFor entry in pygame_events:'+ str(entry))
        if entry.type == 2:   # Keyboard Key Down
            Diag('\tKeyBoardKeyDown:' + str(entry))
            if entry.unicode == '\x03':  # Control + C
                Quit()
            if entry.key == 27:         # Escape Key
                Quit()
            if entry.key == 32:         # Space Bar
                Diag('\t\tentry.key.down # 32 Start!')
                Diag('\t\tentry.key.down # 32 End!')
            try:
                if held_keys['Up'] == True:
                    pass
                else:
                    if entry.key == 273:        # Up Arrow Key
                        Diag('\t\tentry.key.down # 273 Start!')
                        p_rect = GoUp(p_rect, dist=p_speed, hold=True)
                        Diag('\t\tentry.key.down # 273 End!')
            except:
                pass
            try:
                if held_keys['Down'] == True:
                    pass
                else:
                    if entry.key == 274:        # Down Arrow Key
                        Diag('\t\tentry.key.down # 274 Start!')
                        p_rect = GoDown(p_rect, dist=p_speed, hold=True)
                        Diag('\t\tentry.key.down # 274 End!')
            except:
                pass
            try:
                if held_keys['Left'] == True:
                    pass
                else:
                    if entry.key == 276:        # Left Arrow Key
                        Diag('\t\tentry.key.down # 276 Start!')
                        p_rect = GoLeft(p_rect, dist=p_speed, hold=True)
                        Diag('\t\tentry.key.down # 276 End!')
            except:
                pass
            try:
                if held_keys['Right'] == True:
                    pass
                else:
                    if entry.key == 275:        # Right Arrow Key
                        Diag('\t\tentry.key.down # 275 Start!')
                        p_rect = GoRight(p_rect, dist=p_speed, hold=True)
                        Diag('\t\tentry.key.down # 275 End!')
            except:
                pass
        elif entry.type == 3:   # Keyboard Key Up
            Diag('ProcessInputs:KeyBoardKeyUp:'+ str(entry))
            if entry.key == 27:         # Escape Key
                Diag('\t\tentry.key.up # 27 Start!')
                Quit()
                Diag('\t\tentry.key.up # 27 End!')
            if entry.key == 32:         # Space Bar
                Diag('\t\tentry.key.up # 32 Start!')
                global diag_mode            # Toggle Diag Mode
                if diag_mode == True:
                    diag_mode = False
                elif diag_mode == False:
                    diag_mode = True
                Diag('\tSetDiagMode:'+ str(diag_mode))
                Diag('\t\tentry.key.up # 32 End!')
            if entry.key == 273:        # Up Arrow Key
                Diag('\t\tentry.key.up # 273 Start!')
                held_keys['Up'] = False
                Diag('\t\tentry.key.up # 273 End!')
            if entry.key == 274:        # Down Arrow Key
                Diag('\t\tentry.key.up # 274 Start!')
                held_keys['Down'] = False
                Diag('\t\tentry.key.up # 274 End!')
            if entry.key == 276:        # Left Arrow Key
                Diag('\t\tentry.key.up # 276 Start!')
                held_keys['Left'] = False
                Diag('\t\tentry.key.up # 276 End!')
            if entry.key == 275:        # Right Arrow Key
                Diag('\t\tentry.key.up # 275 Start!')
                held_keys['Right'] = False
                Diag('\t\tentry.key.up # 275 End!')
        elif entry.type == 4:     # Mouse Motion
            Diag('ProcessInputs:MouseMotion:'+ str(entry))
            UpdateMouse(entry.pos)
        elif entry.type == 5:   # Mouse Key Down
            Diag('ProcessInputs:MouseKeyDown:'+ str(entry))
            if entry.button == 1:       # Left Mouse Button
                pass
            if entry.button == 2:       # Middle Mouse Button
                pass
            if entry.button == 3:       # Right Mouse Button
                pass
        elif entry.type == 6:   # Mouse Key Up
            Diag('ProcessInputs:MouseKeyUp:'+ str(entry))
            if entry.button == 1:       # Left Mouse Button
                pass
            if entry.button == 2:       # Middle Mouse Button
                pass
            if entry.button == 3:       # Right Mouse Button
                pass




def UpdatePlayerCenter():
    global p_center
    p_center = RectCenter(p_rect)
######################################################

######################################################
# Move Elements
# Move Helpers
    # Input any rectangle(x,y,size_x,size_y), and move it 'dist' number of units up, down, left or right
def GoLeft(rect, dist=1, hold=False):
    if diag_core == True:
        print('\tGoLeft:',rect,':',dist,':',hold)
    global held_keys
    x, y, size_x, size_y = rect
    if hold == True:
        held_keys['Left'] = True
    if x - dist > 0:
        x -= dist
    else:
        x = 0
    return (x, y, size_x, size_y)
def GoRight(rect, dist=1, hold=False):
    if diag_core == True:
        print('\tGoRight:',rect,':',dist,':',hold)
    global held_keys
    x, y, size_x, size_y = rect
    if hold == True:
        held_keys['Right'] = True
    if x + size_x + dist < window_width:
        x += dist
    else:
        x = window_width - size_x
    return (x, y, size_x, size_y)
def GoDown(rect, dist=1, hold=False):
    if diag_core == True:
        print('\tGoDown:',rect,':',dist,':',hold)
    global held_keys
    x, y, size_x, size_y = rect
    if hold == True:
        held_keys['Down'] = True
    if y + size_y + dist < window_height:
        y += dist
    else:
        y = window_height - size_y
    return (x, y, size_x, size_y)
def GoUp(rect, dist=1, hold=False):
    if diag_core == True:
        print('\tGoUp:',rect,':',dist,':',hold)
    global held_keys
    x, y, size_x, size_y = rect
    if hold == True:
        held_keys['Up'] = True
    if y - dist > 0:
        y -= dist
    else:
        y = 0
    return (x, y, size_x, size_y)

# Move Core
def MoveRewards():
    if diag_core == True:
        print('MoveRewards')
    for num, entry in rewards.items():
        MoveReward(rewards[num], rewards_num=num)
def MoveReward(rect, rewards_num, speed=2):
    if diag_core == True:
        print('  MoveReward:',rect,':',rewards_num,':',speed)
    # Do Something
    pass
def MoveEnemies():
    if diag_core == True:
        print('MoveEnemies')
    # Move through the Enemies list and move each enemy rectangle
    for num, entry in enemies.items():
        MoveEnemy(enemies[num], enemies_num=num)
def MoveEnemy(rect, enemies_num, speed=difficulty[player_difficulty]['e_speed']):
    if diag_core == True:
        print('  MoveEnemy:',rect,':',enemies_num,':',speed)
    # Chase Player
    rect = GoToPlayer(rect, speed=speed, chance=70)
    # Grow Enemy size
    enemies[enemies_num] = GrowRect(rect, 1, difficulty[player_difficulty]
                                    ['e_max_size'], difficulty[player_difficulty]['e_growth_rate'])
######################################################

######################################################
# Re-spawn Elements
def RespawnReward(entry_to_replace):
    if diag_core == True:
        print('RespawnReward:',entry_to_replace)
    global rewards
    tmp = {}
    for num, entry in rewards.items():
        adder = 0
        if num == entry_to_replace:
            adder = 1
        elif adder == 1:
            tmp[num - 1] = rewards[num]
        else:
            tmp[num] = rewards[num]
    rewards = tmp
    AddReward()
def RespawnEnemies(count):
    if diag_core == True:
        print('RespawnEnemies:',count)
    global enemies
    enemies = {}
    for x in range(count):
        AddEnemy()
######################################################

######################################################
# Check for Collisions
def PlayerCollideCheck():
    if diag_core == True:
        print('PlayerCollideCheck')
    global p_score
    for num, entry in enemies.items():
        if Collision(enemies[num], p_rect):
            p_score -= 1
    for num, entry in rewards.items():
        if Collision(rewards[num], p_rect):
            p_score += 1
            if p_score % 10 == 0:
                RespawnEnemies(difficulty[player_difficulty]['num_enemies'])
            RespawnReward(num)
    return 'none', 0
def CollideButtons():
    if diag_core == True:
        print('CollideButtons')
    pass
def MouseCollision():
    if diag_core == True:
        print('MouseCollision')
    global b
    for num, entry in b.items():
        #print('Num:',num, '\tCollision:',b[num][0].colliderect(m_loc))
        b[num] = (b[num][0], b[num][1], b[num][2],
                  b[num][0].colliderect(m_loc))
######################################################

######################################################
# Draw Elements
def DrawPlayer():
    Diag('DrawPlayer:'+str(p_rect))
    player = pygame.draw.rect(screen, p_color, p_rect, 0)
def DrawRewards():
    Diag('DrawRewards')
    for num, entry in rewards.items():
        DrawReward(rewards[num])
def DrawReward(rect):
    Diag('DrawReward:'+str(rect))
    reward = pygame.draw.rect(screen, r_color, rect, 0)
def DrawEnemies():
    Diag('DrawEnemies')
    # Move through the Enemies list and draw each enemy rectangle
    for num, entry in enemies.items():
        DrawEnemy(enemies[num])
def DrawEnemy(rect):
    Diag('DrawButtons:'+str(rect))
    enemy = pygame.draw.rect(screen, e_color, rect, 0)
def DrawScore():
    Diag('DrawScore')
    text = monospace_font.render(
        ("Score: " + str(p_score)), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
def DrawControlMode():
    Diag('DrawControlMode')
    text = monospace_font.render(
        ("Control: " + control_mode), 1, (255, 255, 255))
    screen.blit(text, (10, 25))
def DrawButtons():
    Diag('DrawButtons')
    if diag_mode == True:
        for num, entry in b.items():
            #print('Entry: ' + str(num) + '\tRect:',entry[0],'\tColor:',entry[1])
            if b[num][3] == 0:
                buttons[num] = pygame.draw.rect(screen, entry[1], entry[0])
            elif b[num][3] == 1:
                buttons[num] = pygame.draw.rect(screen, entry[2], entry[0])
def DrawButtonClick(num):
    Diag('DrawButtonClick:'+str(num))
    pygame.draw.rect(screen, b[num][2], b[num][0])
    UpdateScreen()
def DrawButtonHover(num):
    Diag('DrawButtonHover:'+str(num))
    buttons[num] = pygame.draw.rect(
        screen, b.items()[num][2], b.items()[num][0])
def DrawPlayerLines():
    Diag('DrawPlayerLines')
    if diag_mode == True:
        for num, entry in rewards.items():
            start = p_center
            end = RectCenter(entry)
            DrawLines(start, end, TEAL)
        for num, entry in enemies.items():
            start = p_center
            end = RectCenter(entry)
            DrawLines(start, end, YELLOW)
def DrawLines(start_rect, end_rect, color):
    Diag('DrawButtonClick:'+str(start_rect)+':'+str(end_rect)+':'+str(color))
    pygame.draw.line(
        screen, color, (start_rect[0], start_rect[1]), (end_rect[0], end_rect[1]))

######################################################

######################################################
# Print Functions
def PrintDicts():
    Diag('PrintDicts')
    print('Rewards:',rewards)
    print('Enemies:',enemies)
    print('b:',b)
    print('Buttons:',buttons)

######################################################

######################################################
# Main
def main():
    Diag('main')

    # Start with X Enemies
    RespawnEnemies(difficulty[player_difficulty]['num_enemies'])

    # Start with 2 Rewards
    AddReward()
    AddReward()
    diag_mode = True

    while True:
        #PrintDicts()
        clock.tick(60)
        GetEvents()
        ProcessInputs()
        UpdatePlayerCenter()
        PlayerCollideCheck()
        MoveRewards()
        MoveEnemies()
        WipeScreen()
        DrawPlayer()
        DrawRewards()
        DrawEnemies()
        DrawButtons()
        DrawScore()
        if diag_mode == True:
            DrawControlMode()
            DrawPlayerLines()
        UpdateScreen()
        ExitCheck()
        #print(clock.get_fps())
        #pygame.time.wait(15)


main()
