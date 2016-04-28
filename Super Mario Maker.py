# Super Mario Maker for PC
# Design, created, and programmed by Hailang Liou, 2016

# hailangliou @ gmail.com
# hliou @ andrew.cmu.edu

# Created for the final term project of CMU 15-112

# Acknowledgements:
# Some elements of event handling framework adapted from code from CA Optional
# lecture on PyGame, however, most is written from scratch by me

# Credit for the spritesheets belong to their respective rippers and are all
# taken from http://www.mariouniverse.com/sprites/snes/smw

# All rights to the Super Mario franchise and its respective characters and
# other assets belong to Nintendo Co., Ltd., and other copyright holders. By
# creating this game, I do not claim ownership of the copyrighted materials
# used within. The creation of this game falls under Fair Use as its role as
# a non-profit, non-commercial, educational work.

import pygame
from pygame.locals import *

import random
import pickle
import os

import player
import enemies
import blocks
import items
import level
import utilities as util

####################################
# INITIALISATION FUNCTIONS
####################################


def init(data):
    data.font = pygame.font.SysFont("", 23)
    data.counter = 0
    data.savedGames = 0
    data.mode = "mainMenu"
    data.keysDown = dict()
    initColours(data)
    initConstants(data)
    initSprites(data)
    initSounds(data)
    initMenu(data)
    initEditor(data)

def initColours(data):
    # basic colours and their rgb values
    data.WHITE = (255, 255, 255)
    data.BLACK = (0, 0, 0)
    data.RED = (255, 0, 0)
    data.BLUE = (0, 0, 255)
    data.BEIGE = (255, 237, 191)

def initConstants(data):
    # list of placeable items and level features
    data.enemyList = ["goomba", "koopa", "redKoopa", "bullet", "blast", "fireball", "thwomp"]
    data.platformList = ["start", "end", "block", "brick", "question", "kaizo", "pipe", "platform", "fallingPlat", "spike"]
    data.itemList = ["mushroom", "flower", "shell"]

def initSprites(data):
    # (row, col) representation of each item within their spritesheets
    data.blockSpritePos = (6, 2)
    data.brickSpritePos = (0, 1)
    data.questionSpritePos = (1, 1)
    data.pipeSpritePos = (3, 4)
    
    data.platformSpritePos1 = (17, 10)
    data.platformSpritePos2 = (17, 11)
    data.platformSpritePos3 = (17, 12)
    data.platformSprites = [data.platformSpritePos1, data.platformSpritePos2, data.platformSpritePos3]

    data.fallingPlatformSpritePos1 = (18, 10)
    data.fallingPlatformSpritePos2 = (18, 11)
    data.fallingPlatformSpritePos3 = (18, 12)
    data.fallingPlatformSprites = [data.fallingPlatformSpritePos1, data.fallingPlatformSpritePos2, data.fallingPlatformSpritePos3]

    data.goombaSpritePos = (0, 0)

    data.mushroomSpritePos = (0, 0)
    data.flowerSpritePos = (0, 2)

def initSounds(data):
    try:
        data.jumpSFX = pygame.mixer.Sound("music/jump.wav")
        data.powerupSFX = pygame.mixer.Sound("music/powerup.wav")
        data.powerdownSFX = pygame.mixer.Sound("music/powerdown.wav")
        data.saveSFX = pygame.mixer.Sound("music/save.wav")
        data.spawnitemSFX = pygame.mixer.Sound("music/spawnitem.wav")
        data.stompSFX = pygame.mixer.Sound("music/stomp.wav")
        data.jumpSFX = pygame.mixer.Sound("music/jump.wav")
        data.fireSFX = pygame.mixer.Sound("music/fireball.wav")
    except:
        pass
    data.clearMusic = "music/clear.wav"
    data.deathMusic = "music/death.wav"
    data.menuMusic = "music/titletheme.wav"
    data.gameMusic = "music/athletic.wav"
    data.gameMusic2 = "music/overworld.wav"


def initMenu(data):
    buttonW, buttonH = 200, 75 # pixels
    buttonX = (data.width / 2) - (buttonW / 2)
    data.menuButtons = list()

    data.backButton = pygame.image.load("images/backbutton.png").convert_alpha()
    data.backButton = pygame.transform.scale(data.backButton, (100, 100))
    data.backButtonRect = data.backButton.get_rect()
    data.menuButtons.append(util.Button(buttonX, 225, 
        buttonW, buttonH, "designer", data))
    data.menuButtons.append(util.Button(buttonX, 325, 
        buttonW, buttonH, "playMenu", data))
    # data.menuButtons.append(util.Button(buttonX, 350, 
    #   buttonW, buttonH, "online", data))

    try:
        pygame.mixer.music.load(data.menuMusic)
        pygame.mixer.music.set_volume(.125)
        pygame.mixer.music.play()
    except:
        pass

def initEditor(data):
    initButtons(data)

    # initialises important constants for the level editor
    # DO NOT MODIFY VALUES
    data.MARGIN = 100
    data.GRID_SIZE = (data.width - data.MARGIN) // 18 # pixels
    
    data.GRID_HEIGHT, data.GRID_WIDTH = 10, 18
    data.LEVEL_HEIGHT, data.LEVEL_WIDTH = 27, 270

    data.SCROLL_TICK_R, data.SCROLL_TICK_L = 0, 0
    data.SCROLL_TICK_U, data.SCROLL_TICK_D = 0, 0
    data.SCROLL_FREQUENCY_R, data.SCROLL_FREQUENCY_L = 10, 10
    data.SCROLL_FREQUENCY_U, data.SCROLL_FREQUENCY_D = 10, 10

    data.mousedButton = False, None

    data.selected  = ""
    data.level = level.Level("SMW")
    data.levelX = 17 # since height is 27 (indexed at 26) and height is 10
    data.xOffsetEditor = 0
    data.yOffsetEditor = 17
    data.onScreen = [[0] * data.LEVEL_WIDTH for row in range(data.LEVEL_HEIGHT)]

    data.actionsList = list()

    data.tilePlaced = False
    data.firstInit = True

def initButtons(data):
    enemyButtons = initEnemyButtons(data)
    blockButtons = initBlockButtons(data)
    itemButtons = initItemButtons(data)
    utilButtons = initUtilButtons(data)

    data.backButton = pygame.image.load("images/backbutton.png").convert_alpha()
    data.backButton = pygame.transform.scale(data.backButton, (100, 100))
    data.backButtonRect = data.backButton.get_rect()

    data.buttonColl = [enemyButtons, blockButtons, itemButtons, utilButtons]

def initEnemyButtons(data):
    # (200, 0) to (1000, 50)
    startx, starty = 200, 0
    size = 30
    buttons = data.enemyList
    data.enemyButtons = list()
    for button in range(len(buttons)):
        image = getButtonImage(data, buttons[button], size)
        x, y = (size * 2 * button + 1) + startx, 10
        data.enemyButtons.append(util.Button(x, y, size, size, 
            buttons[button], data, image = image))
    return data.enemyButtons

def initBlockButtons(data):
    # (200, 50) to (1000, 100)
    startx, starty = 200, 50
    size = 30
    buttons = data.platformList
    data.blockButtons = list()
    for button in range(len(buttons)):
        image = getButtonImage(data, buttons[button], size)
        x, y = (size * 2 * button + 1) + startx, 60
        data.blockButtons.append(util.Button(x, y, size, size, 
            buttons[button], data, image = image))
    return data.blockButtons

def initItemButtons(data):
    # after enemy buttons, so (XXX, 0) to (1000, 50)
    size = 30
    startx, starty = (size * 2 * len(data.enemyList)) + 200, 0
    buttons = data.itemList
    data.itemButtons = list()
    for button in range(len(buttons)):
        image = getButtonImage(data, buttons[button], size)
        x, y = (size * 2 * button + 1) + startx, 10
        data.itemButtons.append(util.Button(x, y, size, size, 
            buttons[button], data, image = image))
    return data.itemButtons

def getButtonImage(data, button, size):
    # gets the image of the object for the buttons on the top
    if(button == "block"):
        return blocks.Block.getSprite(size, size, data.blockSpritePos)
    elif(button == "brick"):
        return blocks.Block.getSprite(size, size, data.brickSpritePos)
    elif(button == "question"):
        return blocks.Block.getSprite(size, size, data.questionSpritePos)
    elif(button == "kaizo"):
        return blocks.Kaizo.getSprite(size, size, data.questionSpritePos)
        # image.fill((255, 255, 255, 40), None, pygame.BLEND_RGBA_MULT)
        # return image
    elif(button == "start"):
        return player.Player.getSmallSquareSprite(size)
    elif(button == "end"):
        return blocks.EndPole.getSquareSprite(size)
    elif(button == "spike"):
        return pygame.transform.scale(pygame.image.load("images/spikes.png").convert_alpha(), (size, size))
    elif(button == "pipe"):
        return blocks.Pipe.getSprite(size)
    elif(button == "platform"):
        return blocks.Platform.getSprite(size, size, data.platformSprites)
    elif(button == "fallingPlat"):
        return blocks.FallingPlatform.getSprite(size, size, data.fallingPlatformSprites)

    if(button == "goomba"):
        return enemies.Goomba.getSprite(size)
    elif(button == "koopa"):
        return enemies.Koopa.getSquareSprite(size)
    elif(button == "redKoopa"):
        return enemies.RedKoopa.getSquareSprite(size)
    elif(button == "thwomp"):
        return enemies.Thwomp.getSquareSprite(size)
    elif(button == "blast"):
        return enemies.Blaster.getSprite(size)
    elif(button == "bullet"):
        return enemies.BulletShooter.getSquareSprite(size)
    elif(button == "fireball"):
        return enemies.Fire.getSprite(size)

    if(button == "mushroom"):
        return items.Mushroom.getSprite(size)
    elif(button == "shell"):
        return items.RedShell.getSprite(size)
    elif(button == "flower"):
        return items.FireFlower.getSprite(size)
    # elif(button == "redShell"):
    #     return items.Mushroom.getSprit(size)

def initUtilButtons(data):
    # (0, 200) to (600, 100)
    startx, starty = 0 , 200
    sizex, sizey = 75, 25
    buttons = ["eraser", "undo", "save", "load", "play"]
    data.utilButtons = list()
    for button in range(len(buttons)):
        x, y = (50 - sizex / 2), (sizey * 2 * button + 1) + starty
        data.utilButtons.append(util.Button(x, y, sizex, sizey, 
            buttons[button], data = data))
    return data.utilButtons

def initPlayer(data, start):

    # initialises important constants for the player
    # DO NOT MODIFY VALUES
    data.PLAY_GRID_SIZE = data.width // 25 # pixels
    data.PLAY_GRID_HEIGHT = data.height // data.PLAY_GRID_SIZE
    data.PLAY_GRID_WIDTH = data.width // data.PLAY_GRID_SIZE

    data.X_SCROLL_MARGIN = data.width // 5
    data.Y_SCROLL_MARGIN = data.height // 6

    data.xOffsetPlay = 0
    data.yOffsetPlay = 12

    data.xOffsetPlayPix = 0
    data.yOffsetPlayPix = 0
    # data.yOffsetPlayPix = data.yOffsetPlay * data.PLAY_GRID_SIZE

    data.player = player.Player(start[0], start[1], data.level.style, data)
    data.playerGroup = pygame.sprite.Group(data.player)
    data.gravity = .7
    data.score = 0
    data.coins = 0

    data.fireballs = 0

    data.bg = blocks.Background(data, (0, 0))
    data.backgroundGroup = pygame.sprite.Group(data.bg)
 

def initLevel(data, level):
    data.gameOverImage = pygame.image.load("images/gameover.png").convert_alpha()
    data.gameOverButton = util.Button(data.width / 2 - 30, 
        data.height / 2 + 100, 60, 25, "restart", data, text = " Restart ")

    data.clearedImage = pygame.image.load("images/cleared.jpg").convert()
    data.winButton = util.Button(data.width / 2 - 60, 
        data.height / 2 + 200, 120, 25, "returnToMenu", data, 
        text = " Return To Menu ")

    data.platformGroup = pygame.sprite.Group()
    data.enemyGroup = pygame.sprite.Group()
    data.itemGroup = pygame.sprite.Group()
    data.fireGroup = pygame.sprite.Group()

    # for each placed element in the level array created in the editor, create
    # the corresponding object for the play map
    levelMap = level.getMap()
    for row in range(len(levelMap)):
        for col in range(len(levelMap[0])):
            if(levelMap[row][col] in data.platformList or 
                levelMap[row][col] in data.enemyList or 
                levelMap[row][col] in data.itemList or
                levelMap[row][col] in ["question1", "question2"]):
                print(levelMap[row][col])
                createMapObject(data, row, col, levelMap[row][col])

def createMapObject(data, row, col, entity):
    # wrapper for object creation
    # question1 and question2 are question mark blocks with mushrooms and
    # flowers, respectively.
    if(entity in data.platformList or entity in ["question1", "question2"]):
        createPlatObject(data, row, col, entity)
    elif(entity in data.enemyList):
        createEnemyObject(data, row, col, entity)
    elif(entity in data.itemList):
        createItemObject(data, row, col, entity)

def createPlatObject(data, row, col, entity):
    if(entity == "block"):
        data.platformGroup.add(blocks.Block(data, row, col, 
            data.blockSpritePos))
    elif(entity == "brick"):
        data.platformGroup.add(blocks.Brick(data, row, col, 
            data.brickSpritePos))
    elif(entity == "question"):
        data.platformGroup.add(blocks.Question(data, row, col, 
            data.questionSpritePos))
    elif(entity == "question1"):
        data.platformGroup.add(blocks.Question(data, row, col, 
            data.questionSpritePos, item = "mushroom"))
    elif(entity == "question2"):
        data.platformGroup.add(blocks.Question(data, row, col, 
            data.questionSpritePos, item = "flower"))
    elif(entity == "kaizo"):
        data.platformGroup.add(blocks.Kaizo(data, row, col, 
            data.questionSpritePos))
    elif(entity == "pipe"):
        data.platformGroup.add(blocks.Pipe(data, row, col, 
            data.pipeSpritePos, 0))
    elif(entity == "platform"):
        data.platformGroup.add(blocks.Platform(data, row, col, 
            data.platformSprites))
    elif(entity == "fallingPlat"):
        data.platformGroup.add(blocks.FallingPlatform(data, row, col, 
            data.fallingPlatformSprites))
    elif(entity == "spike"):
        data.platformGroup.add(blocks.Spike(data, row, col, (0,0)))
    elif(entity == "end"):
        data.platformGroup.add(blocks.EndPole(data, row, col))

def createEnemyObject(data, row, col, entity):
    if(entity == "goomba"):
        data.enemyGroup.add(enemies.Goomba(row, col, False, "left", data))
    elif(entity == "koopa"):
        data.enemyGroup.add(enemies.Koopa(row, col, False, "left", data))
    elif(entity == "redKoopa"):
        data.enemyGroup.add(enemies.RedKoopa(row, col, False, "left", data))
    elif(entity == "thwomp"):
        data.enemyGroup.add(enemies.Thwomp(row, col, data))
    elif(entity == "bullet"):
        data.enemyGroup.add(enemies.BulletShooter(row, col, "left", data))
    elif(entity == "blast"):
        data.enemyGroup.add(enemies.Blaster(row, col, "left", data))
    elif(entity == "fireball"):
        data.enemyGroup.add(enemies.Fire(row, col, data))

def createItemObject(data, row, col, entity):
    if(entity == "mushroom"):
        data.itemGroup.add(items.Mushroom(row, col, data, 
            data.mushroomSpritePos))
    if(entity == "flower"):
        data.itemGroup.add(items.FireFlower(row, col, data, 
            data.mushroomSpritePos))
    elif(entity == "shell"):
        data.itemGroup.add(items.RedShell(row, col, data))



def initPlayMenu(data):
    data.levelList = list()
    fileList = os.listdir("savedata/")
    for file in fileList:
        if(file.endswith(".smm")):
            data.levelList.append(file[:-4])

    # from 250 - 750 x, 150 - 450 y
    data.menuLevelButtonList = list()
    for level in range(len(data.levelList)):
        x = 100 + 100 * (level % 8)
        y = 200 + 100 * (level // 8)
        data.menuLevelButtonList.append(util.Button(x, y, 90, 50, 
            data.levelList[level], data))

def initOnline(data):
    data.loggedIn = False
    data.selectedBox = None
    data.username = None

    width, height = 400, 100
    x = data.width / 2 - width / 2
    data.usernameBox = util.TextBox(x, data.height / 2 - height, width, 
        height, "user", data)
    data.passwordBox = util.TextBox(x, data.height / 2 + height, width, 
        height, "pw", data, True)
    data.loginBoxes = [data.usernameBox, data.passwordBox]


#######################################
# EVENT HANDLING FRAMEWORK (WRAPPER)
#######################################



def controller(data):
    for event in pygame.event.get():
        if(event.type == QUIT): return False
        elif(event.type == KEYDOWN):
            data.keysDown[event.key] = True
            keyPressed(event.key, data)
        elif(event.type == KEYUP):
            data.keysDown[event.key] = False
            keyReleased(event, data)
        elif(event.type == MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif(event.type == MOUSEMOTION and event.buttons[0] == 1):
            mouseDragged(event, data)
        elif(event.type == MOUSEMOTION):
            mouseMoved(event, data)

def keyPressed(key, data):
    if(data.mode == "designer"):
        designKeyPressed(key, data)
    elif(data.mode == "play"):
        playKeyPressed(key, data)
    elif(data.mode == "save"):
        saveKeyPressed(key, data)
    elif(data.mode == "load"):
        loadKeyPressed(key, data)
    elif(data.mode == "online"):
        onlineKeyPressed(key, data)

def keyHeld(key, data):
    if(data.mode == "designer"):
        designerKeyHeld(key, data)
    elif(data.mode == "play"):
        playKeyHeld(key, data)

def keyReleased(key, data):
    if(data.mode == "designer"):
        if(key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]):
            stopKeyScroll(key, data)
    elif(data.mode == "play"):
        playKeyReleased(key, data)

def mousePressed(event, data):
    if(data.mode == "mainMenu"):
        mainMenuClicked(event.pos, data)
    elif((data.mode) == "designer"):
        designerClicked(event.pos, data)
    elif(data.mode == "gameOver"):
        gameOverClicked(event.pos, data)
    elif(data.mode == "save"):
        saveClicked(event.pos, data)
    elif(data.mode == "load"):
        loadClicked(event.pos, data)
    elif(data.mode == "playMenu"):
        playMenuClicked(event.pos, data)
    elif((data.mode) == "online"):
        onlineClicked(event.pos, data)
    elif(data.mode == "winScreen"):
        winClicked(event.pos, data)

def mouseDragged(event, data):
    if((data.mode) == "designer"):
        designerDragged(event.pos, data)

def mouseMoved(event, data):
    if(data.mode == "mainMenu"):
        mainMenuMouseMoved(event.pos, data)
    elif(data.mode == "save"):
        saveMouseMoved(event.pos, data)
    elif(data.mode == "load"):
        loadMouseMoved(event.pos, data)
    elif(data.mode == "playMenu"):
        playMenuMouseMoved(event.pos, data)

def timerFired(data, time):
    for key in data.keysDown:
        if(data.keysDown[key]):
            keyHeld(key, data)
    if(data.mode == "play"):
        data.player.updateEvent(data, None, "timerFired")
    # print(data.counter)
    data.counter += 1



#######################################
# EVENT HANDLING FRAMEWORK (MENU)
#######################################


def mainMenuClicked(pos, data):
    for button in data.menuButtons:
        if(button.buttonRect.collidepoint(pos)):
            if(button.name == "designer"):
                data.saveSFX.play()
                data.mode = "designer"
            elif(button.name == "playMenu"):
                data.saveSFX.play()
                data.mode = "playMenu"
                initPlayMenu(data)
            # elif(button.name == "online"):
            #     data.mode = "online"
            #     initOnline(data)

def mainMenuMouseMoved(pos, data):
    over = False
    for button in data.menuButtons:
        if(button.buttonRect.collidepoint(pos)):
            over = True
            data.mousedButton = True, button
    if(over == False):
        data.mousedButton = False, None


#######################################
# EVENT HANDLING FRAMEWORK (DESIGNER)
#######################################


def designKeyPressed(key, data):
    if(key == K_RIGHT and 
        data.xOffsetEditor < data.LEVEL_WIDTH - data.GRID_WIDTH):
        print('asasa')
        data.xOffsetEditor += 1
    elif(key == K_LEFT and data.xOffsetEditor > 0):
        data.xOffsetEditor -= 1
    elif(key == K_UP and data.yOffsetEditor> 0):
        data.yOffsetEditor -= 1
    elif(key == K_DOWN and 
        data.yOffsetEditor < data.LEVEL_HEIGHT - data.GRID_HEIGHT):
        data.yOffsetEditor += 1


def designerKeyHeld(key, data):
    if(key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]):
        keyScroll(key, data)

def keyScroll(key, data):
    data.tilePlaced = True
    if(key == K_RIGHT and 
        data.xOffsetEditor < data.LEVEL_WIDTH - data.GRID_WIDTH):
        if(data.SCROLL_TICK_R % data.SCROLL_FREQUENCY_R == 0):
            data.xOffsetEditor += 1
        data.SCROLL_TICK_R += 1
        if(data.SCROLL_TICK_R % 30 and data.SCROLL_FREQUENCY_R > 5):
            data.SCROLL_FREQUENCY_R -= 1

    elif(key == K_LEFT and data.xOffsetEditor > 0):
        if(data.SCROLL_TICK_L % data.SCROLL_FREQUENCY_L == 0):
            data.xOffsetEditor -= 1
        data.SCROLL_TICK_L += 1
        if(data.SCROLL_TICK_L % 30 and data.SCROLL_FREQUENCY_L > 5):
            data.SCROLL_FREQUENCY_L -= 1

    elif(key == K_UP and data.yOffsetEditor > 0):
        if(data.SCROLL_TICK_U % data.SCROLL_FREQUENCY_U == 0):
            data.yOffsetEditor -= 1
        data.SCROLL_TICK_U += 1
        if(data.SCROLL_TICK_U % 30 and data.SCROLL_FREQUENCY_U > 5):
            data.SCROLL_FREQUENCY_U -= 1

    elif(key == K_DOWN and 
        data.yOffsetEditor < data.LEVEL_HEIGHT - data.LEVEL_WIDTH):
        if(data.SCROLL_TICK_D % data.SCROLL_FREQUENCY_D == 0):
            data.yOffsetEditor += 1
        data.SCROLL_TICK_D += 1
        if(data.SCROLL_TICK_D % 30 and data.SCROLL_FREQUENCY_D > 5):
            data.SCROLL_FREQUENCY_D -= 1


def stopKeyScroll(key, data):
    if(key == K_RIGHT):
        data.SCROLL_TICK_R = 0
        data.SCROLL_FREQUENCY_R = 10
    elif(key == K_LEFT):
        data.SCROLL_TICK_L = 0
        data.SCROLL_FREQUENCY_L = 10
    elif(key == K_UP):
        data.SCROLL_TICK_U = 0
        data.SCROLL_FREQUENCY_U = 10
    elif(key == K_DOWN):
        data.SCROLL_TICK_D = 0
        data.SCROLL_FREQUENCY_D = 10

def designerClicked(pos, data):
    data.tilePlaced = True
    (x, y) = pos
    if(util.getCell(data, pos[0], pos[1]) != None):
        col, row = util.getCell(data, pos[0], pos[1])
        workareaClicked(data, row, col)
    elif(data.backButtonRect.collidepoint(pos)):
        data.mode = "mainMenu"
    else:
        for buttonSet in data.buttonColl:
            for button in buttonSet:
                if(button.buttonRect.collidepoint(pos)):
                    buttonAction(data, button)

def buttonAction(data, button):
    name = button.getName()
    if(name == "save"):
        save(data)
    elif(name == "load"):
        load(data)
    elif(name == "undo"):
        undo(data)
    elif(name == "play"):
        play(data)
    elif(name == "upload"):
        upload(data)
    elif(name == "style"):
        changeStyle(data)
    else:
        data.selected = name
    print(data.selected)

def save(data):
    data.mode = "save"

    data.saveTextSelected = False
    data.savePopUp = pygame.Surface((data.width // 2, data.height // 2))
    data.popupRect = pygame.Rect(data.width // 4, data.height // 4, 
        data.width // 2, data.height // 2)
    data.savePopUp.fill((255, 237, 191))

    data.saveConfirm = util.Button(400, 400, 50, 25, " Confirm ", data)
    data.saveCancel = util.Button(550, 400, 50, 25, " Cancel ", data)

    data.saveButtons = [data.saveConfirm, data.saveCancel]

    data.saveTextBox = util.TextBox(350, 300, 300, 50, "save", data)


def load(data):
    data.mode = "load"

    data.loadPopUp = pygame.Surface((data.width // 2, data.height // 2))
    data.popupRect = pygame.Rect(data.width // 4, data.height // 4, 
        data.width // 2, data.height // 2)
    data.loadPopUp.fill((255, 237, 191))

    data.levelList = list()
    fileList = os.listdir("savedata/")
    for file in fileList:
        if(file.endswith(".smm")):
            data.levelList.append(file[:-4])

    # from 250 - 750 x, 150 - 450 y
    data.levelButtonList = list()
    print(data.levelList)
    for level in range(len(data.levelList)):
        x = 275 + 100 * (level % 4)
        y = 250 + 100 * (level // 4)
        data.levelButtonList.append(util.Button(x, y, 90, 50, 
            data.levelList[level], data))


def undo(data):
    if(data.actionsList != []):
        action = data.actionsList.pop()
        if(action[3] == 1):
            removeEntity(data, action[1], action[2])
        elif(action[3] == 0):
            data.level.setEntity("over", action[0], action[1], action[2])

def play(data):
    playGame(data, data.level)

def upload(data):
    pass

def changeStyle(data):
    pass

def workareaClicked(data, row, col):
    if(data.selected == "eraser"):
        data.actionsList.append((data.level.getMap()[row][col], row, col, 0))
        removeEntity(data, row, col)
    elif(data.selected != ""):
        data.actionsList.append((data.selected, row, col, 1))
        placeEntity(data, row, col)

def placeEntity(data, row, col):
    if(data.level.getCurrent() == "over"):
        data.level.setEntity("over", data.selected, row, col)
    elif(data.level.getCurrent() == "water"):
        data.level.setEntity("water", data.selected, row, col)
    elif(data.level.getCurrent() == "under"):
        data.level.setEntity("under", data.selected, row, col)

def removeEntity(data, row, col):
    if(data.level.getCurrent() == "over"):
        data.level.setEntity("over", 0, row, col)
    elif(data.level.getCurrent() == "water"):
        data.level.setEntity("water", 0, row, col)
    elif(data.level.getCurrent() == "under"):
        data.level.setEntity("under", 0, row, col)


def designerDragged(pos, data):
    (x, y) = pos
    if(util.getCell(data, x, y) != None):
        col, row = util.getCell(data, x, y)
        if(data.selected == "eraser"):
            data.tilePlaced = True
            removeEntity(data, row, col)
        elif(data.selected != ""):
            data.tilePlaced = True
            placeEntity(data, row, col)


#######################################
# EVENT HANDLING FRAMEWORK (SAVE/LOAD)
#######################################

def saveKeyPressed(key, data):
    if(data.saveTextSelected):
        letter = pygame.key.name(key)
        if(304 in data.keysDown and data.keysDown[304]):
            letter = letter.upper()
        data.saveTextBox.inputText(letter)

def saveClicked(pos, data):
    if(not data.popupRect.collidepoint(pos)):
        data.mode = "designer"
    if(data.saveTextBox.textBoxRect.collidepoint(pos)):
        data.saveTextSelected = True
    else:
        data.saveTextSelected = False

    if(data.saveTextBox.text != "" and data.saveConfirm.buttonRect.collidepoint(pos)):
        saveData = [data.level.overBoard, data.level.underBoard, data.level.waterBoard, 
        "SMW", 0, 0]
        pickle.dump(saveData, open("savedata/%s.smm" % data.saveTextBox.text, "wb+"))
        data.saveSFX.play()
        data.mode = "designer"
    elif(data.saveCancel.buttonRect.collidepoint(pos)):
        data.mode = "designer"

def saveMouseMoved(pos, data):
    over = False
    for button in data.saveButtons:
        if(button.buttonRect.collidepoint(pos)):
            over = True
            data.mousedButton = True, button
    if(over == False):
        data.mousedButton = False, None

def loadKeyPressed(key, data):
    over = False
    for button in data.menuButtons:
        if(button.buttonRect.collidepoint(pos)):
            over = True
            data.mousedButton = True, button
    if(over == False):
        data.mousedButton = False, None

def loadClicked(pos, data):
    if(not data.popupRect.collidepoint(pos)):
        data.mode = "designer"
    for button in data.levelButtonList:
        if(button.buttonRect.collidepoint(pos)):
            saveData = pickle.load(open("savedata/%s.smm" % button.name, "rb+"))
            loadedLevel = level.Level("SMW")
            loadedLevel.loadFromSave(saveData)
            data.level = loadedLevel
            data.saveSFX.play()
            data.mode = "designer"

def loadMouseMoved(pos, data):
    over = False
    for button in data.levelButtonList:
        if(button.buttonRect.collidepoint(pos)):
            over = True
            data.mousedButton = True, button
    if(over == False):
        data.mousedButton = False, None


#######################################
# EVENT HANDLING FRAMEWORK (PLAY)
#######################################


def playGame(data, level):
    start = level.getStart()
    if(start != None):
        data.mode = "play"

        music = random.choice([data.gameMusic, data.gameMusic2])
        try:
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(.125)
            pygame.mixer.music.play()
        except:
            pass

        data.screen.fill(data.WHITE)
        initPlayer(data, start)
        initLevel(data, level)

def playKeyPressed(key, data):
    data.player.updateEvent(data, key, "keyPress")

def playKeyHeld(key, data):
    data.player.updateEvent(data, key, "keyHeld")

def playKeyReleased(key, data):
    data.player.updateEvent(data, key, "keyReleased")


def gameOverClicked(pos, data):
    print(data.gameOverButton.buttonRect)
    if(data.gameOverButton.buttonRect.collidepoint(pos)):
        playGame(data, data.level)

def winClicked(pos, data):
    if(data.winButton.buttonRect.collidepoint(pos)):
        data.mode = "designer"
        try:
            pygame.mixer.music.load(data.menuMusic)
            pygame.mixer.music.set_volume(.125)
            pygame.mixer.music.play()
        except:
            pass


def playMenuClicked(pos, data):
    if(data.backButtonRect.collidepoint(pos)):
        data.saveSFX.play()
        data.mode = "mainMenu"
    else:
        for button in data.menuLevelButtonList:
            if(button.buttonRect.collidepoint(pos)):
                data.saveSFX.play()
                saveData = pickle.load(open("savedata/%s.smm" % button.name, "rb+"))
                loadedLevel = level.Level("SMW")
                loadedLevel.loadFromSave(saveData)
                data.level = loadedLevel
                data.saveSFX.play()
                data.mode = "play"
                play(data)

def playMenuMouseMoved(pos, data):
    over = False
    for button in data.menuLevelButtonList:
        if(button.buttonRect.collidepoint(pos)):
            over = True
            data.mousedButton = True, button
    if(over == False):
        data.mousedButton = False, None


#######################################
# EVENT HANDLING FRAMEWORK (ONLINE)
#######################################


def onlineKeyPressed(key, data):
    if(data.selectedBox != None):
        letter = pygame.key.name(key)
        if(304 in data.keysDown and data.keysDown[304]):
            letter = letter.upper()
        print(letter)
        data.selectedBox.inputText(letter)

def onlineClicked(pos, data):
    clicked = False
    for box in data.loginBoxes:
        if(box.textBoxRect.collidepoint(pos)):
            data.selectedBox = box
            clicked = True
    if(clicked == False):
        data.selectedBox = None


####################################
# DRAWING FRAMEWORK
####################################



def draw(data):
    if(data.mode == "mainMenu"):
        drawMenu(data)
    elif(data.mode == "designer"):
        drawDesigner(data)
    elif(data.mode == "playMenu"):
        drawPlayMenu(data)
    elif(data.mode == "play"):
        drawPlay(data)
    elif(data.mode == "gameOver"):
        drawGameOver(data)
    elif(data.mode == "save"):
        drawSave(data)
    elif(data.mode == "load"):
        drawLoad(data)
    elif(data.mode == "playMenu"):
        drawPlayMenu(data)
    elif(data.mode == "online"):
        drawOnline(data)
    elif(data.mode == "winScreen"):
        drawWinScreen(data)

def paintSurface(data, x, y, width, height, colour):
    surf = pygame.Surface((width, height))
    surf.fill(colour)
    data.screen.blit(surf, (x, y))

def clearSurface(data, x, y, width, height):
    paintSurface(data, x, y, width, height, data.WHITE)

def drawMenu(data):
    drawBG(data)
    drawMenuButtons(data)
    pygame.display.update()

def drawBG(data):
    cx, cy = data.width / 2, data.height / 2
    image = pygame.image.load("images/menu.jpg").convert_alpha()
    data.screen.blit(image, (0, 0))

def drawMenuButtons(data):
    font = pygame.font.SysFont("", 40)
    for button in data.menuButtons:
        bWidth, bHeight = button.buttonRect.width, button.buttonRect.height
        buttonImage = pygame.Surface((bWidth, bHeight))
        buttonImage.fill(data.BEIGE)
        if(button.name == "designer"):
            name = "Create"
        elif(button.name == "playMenu"):
            name = "Play"
        elif(button.name == "online"):
            name = "Online"
        buttonName = font.render(name, True, data.BLACK)
        nameRect = buttonName.get_rect()
        x, y = bWidth / 2 - nameRect.width / 2, bHeight / 2 - nameRect.height / 2
        textRect = (x, y, nameRect.width, nameRect.height)
        buttonImage.blit(buttonName, textRect)
        pygame.draw.rect(buttonImage, data.BLACK, (0, 0, bWidth, bHeight), 2)
        data.screen.blit(buttonImage, button.buttonRect)

    if(data.mousedButton[0] == True):
        highlight = pygame.Surface((data.mousedButton[1].rect.width, 
            data.mousedButton[1].rect.height))
        highlight.set_alpha(100)
        highlight.fill((0, 0, 192))
        pygame.draw.rect(data.screen, data.BLUE, 
            data.mousedButton[1].buttonRect, 2)
        data.screen.blit(highlight, data.mousedButton[1].buttonRect)
        # pygame.draw.rect(buttonImage, data.BLACK, )
        # pygame.draw.rect(data.screen, 0xAAAAAA, button.buttonRect, 2)


def drawDesigner(data):
    # in order from bottom layer to top layer
    drawGrid(data)
    drawEditorButtons(data)
    drawEditor(data)
    pygame.display.update()

def drawGrid(data):
    # redraws only if work area is modified or edge case of initial rendering
    if(data.firstInit or data.tilePlaced):
        data.screen.fill((66, 179, 232))
        data.firstInit = False

        TILE_SPRITES = util.SpriteSheet("images/backgrounds.png")

        image = pygame.Surface((data.width - 100, data.height - 100))
        
        bg = TILE_SPRITES.extractSpriteGrid((0, 0), 512, 432, 2)
        bg = pygame.transform.scale(bg, (593, data.height - 100))
        bgW, bgH = bg.get_width(), bg.get_height()

        x = 0 - (.2 * data.xOffsetEditor * data.GRID_SIZE)
        while (x < data.width):
            image.blit(bg, (x, 0, bgW, bgH))
            x += bgW

        data.screen.blit(image, (100, 100))

        # paintSurface(data, 100, 100, 900, 500, (66, 179, 232))
        pairs = list()
        for row in range(data.GRID_HEIGHT):
            pairs.append(((data.MARGIN, data.MARGIN + row * data.GRID_SIZE), 
                (data.width, data.MARGIN + row * data.GRID_SIZE)))
        for col in range(data.GRID_WIDTH):
            pairs.append(((data.MARGIN + col * data.GRID_SIZE, data.MARGIN), 
                (data.MARGIN + col * data.GRID_SIZE, data.height)))
        for pair in pairs:
            pygame.draw.line(data.screen, 0x000000, pair[0], pair[1])
    # pygame.draw.line(data.screen, 0x000000, (data.width - 1, data.MARGIN), (data.width - 1, data.height), 2)
    # pygame.draw.line(data.screen, 0x000000, (data.MARGIN, data.height - 1), (data.width, data.height - 1), 2)

def drawEditorButtons(data):
    data.screen.blit(data.backButton, data.backButtonRect)
    for button in data.enemyButtons:
        button.draw(data)
        pygame.draw.rect(data.screen, 0xAAAAAA, button.buttonRect, 4)
        if(data.selected == button.getName()):
            pygame.draw.rect(data.screen, 0xFF0000, button.buttonRect, 2)
    for button in data.blockButtons:
        button.draw(data)
        pygame.draw.rect(data.screen, 0xAAAAAA, button.buttonRect, 4)
        if(data.selected == button.getName()):
            pygame.draw.rect(data.screen, 0xFF0000, button.buttonRect, 2)
    for button in data.itemButtons:
        button.draw(data)
        pygame.draw.rect(data.screen, 0xAAAAAA, button.buttonRect, 4)
        if(data.selected == button.getName()):
            pygame.draw.rect(data.screen, 0xFF0000, button.buttonRect, 2)
    for button in data.utilButtons:
        button.draw(data)
        pygame.draw.rect(data.screen, 0xAAAAAA, button.buttonRect, 4)
        if(data.selected == button.getName()):
            pygame.draw.rect(data.screen, 0xFF0000, button.buttonRect, 2)

def drawEditor(data):

    def getImage(entity, data, row, col):
        if(entity == "block"):
            return blocks.Block.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.blockSpritePos)
        elif(entity == "brick"):
            return blocks.Block.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.brickSpritePos)
        elif(entity == "question"):
            return blocks.Block.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.questionSpritePos)
        elif(entity == "kaizo"):
            return blocks.Kaizo.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.questionSpritePos)
        elif(entity == "question1"):
            image = blocks.Block.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.questionSpritePos)
            width, height = image.get_width(), image.get_height()
            size = data.GRID_SIZE // 4
            image.blit(items.Item.getSprite(data.mushroomSpritePos, 
                data.GRID_SIZE // 2), (width / 2 - size, height / 2 - size))
            return image
        elif(entity == "question2"):
            image = blocks.Block.getSprite(data.GRID_SIZE, data.GRID_SIZE, 
                data.questionSpritePos)
            width, height = image.get_width(), image.get_height()
            size = data.GRID_SIZE // 4
            image.blit(items.FireFlower.getSprite(data.GRID_SIZE // 2), 
                (width / 2 - size, height / 2 - size))
            return image
        elif(entity == "pipe"):
            if(data.level.getMap()[row - 1][col] == "pipe"):
                return blocks.Pipe.getPipeBody(data.GRID_SIZE)
            elif(data.level.getMap()[row - 1][col] == "block"):
                return blocks.Pipe.getUpsideDownPipe(data.GRID_SIZE)
            else:
                return blocks.Pipe.getSprite(data.GRID_SIZE)
        elif(entity == "start"):
            return player.Player.getSuperSquareSprite(data.GRID_SIZE)
        elif(entity == "end"):
            return blocks.EndPole.getSprite(data.GRID_SIZE)
        elif(entity == "spike"):
            return blocks.Spike.getSprite(data.GRID_SIZE)
        elif(entity == "platform"):
            return blocks.Platform.getFullSprite(data.GRID_SIZE, 
                data.platformSprites)
        elif(entity == "fallingPlat"):
            return blocks.FallingPlatform.getFullSprite(data.GRID_SIZE, 
                data.fallingPlatformSprites)

        if(entity == "mushroom"):
            return items.Mushroom.getSprite(data.GRID_SIZE)
        elif(entity == "flower"):
            return items.FireFlower.getSprite(data.GRID_SIZE)
        elif(entity == "shell"):
            return items.RedShell.getSprite(data.GRID_SIZE)

        if(entity == "goomba"):
            return enemies.Goomba.getSprite(data.GRID_SIZE)
        elif(entity == "koopa"):
            return enemies.Koopa.getSquareSprite(data.GRID_SIZE)
        elif(entity == "redKoopa"):
            return enemies.RedKoopa.getSquareSprite(data.GRID_SIZE)
        elif(entity == "thwomp"):
            return enemies.Thwomp.getSquareSprite(2 * data.GRID_SIZE)
        elif(entity == "blast"):
            return enemies.Blaster.getSprite(data.GRID_SIZE)
        elif(entity == "bullet"):
            return enemies.BulletShooter.getSquareSprite(data.GRID_SIZE)
        elif(entity == "fireball"):
            return enemies.Fire.getSprite(data.GRID_SIZE)



    for row in range(data.yOffsetEditor, data.yOffsetEditor + data.GRID_HEIGHT):
        for col in range(data.xOffsetEditor, data.xOffsetEditor + data.GRID_WIDTH):
            if(data.level.getMap()[row][col] != 0):
                entity = data.level.getMap()[row][col]
                image = getImage(entity, data, row, col)
                if(entity == "end"):
                    tile = Rect(data.MARGIN + (col - data.xOffsetEditor) * data.GRID_SIZE, 
                    data.MARGIN + (row - 2 - data.yOffsetEditor) * data.GRID_SIZE,
                    data.GRID_SIZE, data.GRID_SIZE)
                elif(entity == "platform" or entity == "fallingPlat"):
                    tile = Rect(data.MARGIN + (col - 1 - data.xOffsetEditor) * data.GRID_SIZE, 
                    data.MARGIN + (row - data.yOffsetEditor) * data.GRID_SIZE,
                    data.GRID_SIZE, data.GRID_SIZE)
                else:    
                    tile = Rect(data.MARGIN + (col - data.xOffsetEditor) * data.GRID_SIZE, 
                        data.MARGIN + (row - data.yOffsetEditor) * data.GRID_SIZE,
                        data.GRID_SIZE, data.GRID_SIZE)

                if(image != None):
                    data.screen.blit(image, tile)
                else:
                    name = data.font.render(data.level.getMap()[row][col], 
                        True, data.BLACK)
                    pygame.draw.rect(data.screen, 0xAAAAAA, tile, 5)
                    data.screen.blit(name, tile)

def drawPlayMenu(data):
    data.screen.fill(data.WHITE)


def drawPlay(data):
    # drawBlocks(data)
    # pygame.draw.rect(data.screen, 0xAAAAAA, data.player.rect, 5)
    data.screen.fill(data.WHITE)

    data.backgroundGroup.update(data)
    data.backgroundGroup.draw(data.screen)

    data.platformGroup.update(data)
    data.platformGroup.draw(data.screen)
    
    data.playerGroup.draw(data.screen)

    data.enemyGroup.update(data)
    data.enemyGroup.draw(data.screen)

    data.itemGroup.update(data)
    data.itemGroup.draw(data.screen)

    data.fireGroup.update(data)
    data.fireGroup.draw(data.screen)

    pygame.display.update()
    # pygame.display.flip()

def drawBlocks(data):
    data.screen.fill(data.WHITE)
    for row in range(data.yOffsetPlay, data.yOffsetPlay + data.PLAY_GRID_HEIGHT):
        for col in range(data.xOffsetPlay, data.xOffsetPlay + data.PLAY_GRID_WIDTH):
            if(data.level.getMap()[row][col] != 0):
                tile = Rect((col - data.xOffsetPlay) * data.PLAY_GRID_SIZE, 
                    (row - data.yOffsetPlay) * data.PLAY_GRID_SIZE,
                    data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE)
                name = data.font.render(data.level.getMap()[row][col], True, data.BLACK)
                pygame.draw.rect(data.screen, 0xAAAAAA, tile, 5)
                data.screen.blit(name, tile)

def drawGameOver(data):
    data.screen.fill(data.WHITE)
    data.screen.blit(data.gameOverImage, (0, 0))
    data.gameOverButton.draw(data)
    pygame.draw.rect(data.screen, data.BLACK, 
        data.gameOverButton.buttonRect, 2)
    pygame.display.update()

def drawWinScreen(data):
    data.screen.fill(data.WHITE)
    data.screen.blit(data.clearedImage, (0, 0))
    pygame.draw.rect(data.screen, data.BLACK, 
        data.winButton.buttonRect, 2)
    data.winButton.draw(data)
    pygame.display.update()

def drawSave(data):
    font = pygame.font.SysFont("", 40)
    text = font.render("Enter level name:", True, data.BLACK)
    width, height = text.get_width(), text.get_height()

    pygame.draw.rect(data.savePopUp, data.BLACK, (0, 0, 500, 300), 2)
    data.savePopUp.blit(text, (250 - width / 2, 50))
    
    data.screen.blit(data.savePopUp, (data.width // 4, data.height // 4))
    pygame.draw.rect(data.screen, data.BLACK, data.saveTextBox.textBoxRect, 5)

    data.saveConfirm.draw(data)
    pygame.draw.rect(data.screen, data.BLACK, data.saveConfirm.buttonRect, 1)
    data.saveCancel.draw(data)
    pygame.draw.rect(data.screen, data.BLACK, data.saveCancel.buttonRect, 1)
    data.saveTextBox.update(data)
    data.saveTextBox.draw(data)

    if(data.mousedButton[0] == True):
        highlight = pygame.Surface((data.mousedButton[1].rect.width, 
            data.mousedButton[1].rect.height))
        highlight.set_alpha(100)
        highlight.fill((0, 0, 192))
        pygame.draw.rect(data.screen, data.BLUE, 
            data.mousedButton[1].buttonRect, 2)
        data.screen.blit(highlight, data.mousedButton[1].buttonRect)

    pygame.display.update()

def drawLoad(data):
    font = pygame.font.SysFont("", 40)
    text = font.render("Select Level:", True, data.BLACK)
    width, height = text.get_width(), text.get_height()

    pygame.draw.rect(data.loadPopUp, data.BLACK, (0, 0, 500, 300), 2)
    data.loadPopUp.blit(text, (250 - width / 2, 50))
    
    data.screen.blit(data.loadPopUp, (data.width // 4, data.height // 4))

    for button in data.levelButtonList:
        button.draw(data)
        pygame.draw.rect(data.screen, data.BLACK, button.buttonRect, 2)

    if(data.mousedButton[0] == True):
        highlight = pygame.Surface((data.mousedButton[1].rect.width, 
            data.mousedButton[1].rect.height))
        highlight.set_alpha(100)
        highlight.fill((0, 0, 192))
        pygame.draw.rect(data.screen, data.BLUE, 
            data.mousedButton[1].buttonRect, 2)
        data.screen.blit(highlight, data.mousedButton[1].buttonRect)

    pygame.display.update()

def drawPlayMenu(data):

    image = pygame.image.load("images/menu.jpg").convert_alpha()
    data.screen.blit(image, (0, 0))

    image = pygame.image.load("images/levelselect2.png").convert_alpha()
    width = image.get_width()
    data.screen.blit(image, (data.width // 2 - width // 2, 50))

    data.screen.blit(data.backButton, data.backButtonRect)

    for button in data.menuLevelButtonList:
        button.draw(data)
        pygame.draw.rect(data.screen, data.BLACK, button.buttonRect, 2)

    if(data.mousedButton[0] == True):
        highlight = pygame.Surface((data.mousedButton[1].rect.width, 
            data.mousedButton[1].rect.height))
        highlight.set_alpha(100)
        highlight.fill((0, 0, 192))
        pygame.draw.rect(data.screen, data.BLUE, data.mousedButton[1].buttonRect, 2)
        data.screen.blit(highlight, data.mousedButton[1].buttonRect)

    pygame.display.update()

def drawOnline(data):
    data.screen.fill(data.WHITE)

    if(not data.loggedIn):
        drawLoginScreen(data)
    pygame.display.update()

def drawLoginScreen(data):
    for box in data.loginBoxes:
        box.update(data)
        box.draw(data)
        if(box == data.selectedBox):
            pygame.draw.rect(data.screen, data.RED, box.textBoxRect, 2)    
        else:
            pygame.draw.rect(data.screen, 0xAAAAAA, box.textBoxRect, 2)


####################################
# RUN FRAMEWORK
####################################



def run(width = 1000, height = 600):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    class Struct(object): pass
    data = Struct()
    data.width, data.height = width, height

    data.screen = pygame.display.set_mode((width, height))

    init(data)

    pygame.display.set_caption("Super Mario Maker")
    data.screen.fill(data.WHITE)
    pygame.display.flip()

    while(True):
        time = clock.tick(60) # frames per second
        timerFired(data, time)
        if(controller(data) == False): return
        draw(data)

run(1000, 600)