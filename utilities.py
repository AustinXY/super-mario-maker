import pygame
from pygame.locals import *

import string
import blocks

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, name, data, color = "white", text = "", imageCoords = None, image = None, textColor = "black"):
        super().__init__()
        self.buttonRect = Rect(x, y, width, height)
        self.rect = self.buttonRect

        self.name = name
        self.text = text

        if(textColor == "black"):
            self.textColor = data.BLACK
        elif(textColor == "white"):
            self.textColor = data.WHITE

        if(image != None):
            self.image = image
            self.image = pygame.transform.scale(self.image, (width, height))

        # if(imageCoords != None):
        #     self.image = blocks.Block.getSprite(width, height, imageCoords)
        #     self.image = pygame.transform.scale(self.image, (width, height))
        else:
            if(self.text != ""):
                name = self.text

            self.image = pygame.Surface((width, height))

            bWidth, bHeight = self.rect.width, self.rect.height
            self.image.fill((255, 237, 191))

            font = pygame.font.SysFont("Helvetica, Arial", 16)
            buttonName = font.render(name, True, self.textColor)
            nameRect = buttonName.get_rect()
            nameX, nameY = bWidth / 2 - nameRect.width / 2, bHeight / 2 - nameRect.height / 2
            textRect = (nameX, nameY, nameRect.width, nameRect.height)
            self.image.blit(buttonName, textRect)

    def getName(self):
        return self.name

    def draw(self, data):
        data.screen.blit(self.image, self.buttonRect)

class TextBox(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, name, data, starred = False):
        super().__init__()
        self.textBoxRect = Rect(x, y, width, height)
        self.rect = self.textBoxRect

        self.name = name
        self.text = ""
        self.starred = starred
    
        self.image = pygame.Surface((width, height))

        bWidth, bHeight = self.rect.width, self.rect.height
        self.image.fill((255, 237, 191))

        self.font = pygame.font.SysFont("Helvetica, Arial", 20)

    def inputText(self, key):
        if(key in string.ascii_letters or 
            key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
            self.text += key
        elif(key == "backspace"):
            self.text = self.text[:-1]

    def update(self, data):
        # self.image.fill((255, 237, 191))
        self.image.fill(data.WHITE)
        bWidth, bHeight = self.rect.width, self.rect.height
        if(self.starred):
            textLen = len(self.text)
            text = self.font.render("*" * textLen, True, data.BLACK)
        else:
            text = self.font.render(self.text, True, data.BLACK)
        textRect = text.get_rect()
        textX, textY = bWidth / 2 - textRect.width / 2, bHeight / 2 - textRect.height / 2
        textRect = (textX, textY, textRect.width, textRect.height)
        self.image.blit(text, textRect)

    def draw(self, data):
        data.screen.blit(self.image, self.textBoxRect)

class DialogBox(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super.__init__()

class SpriteSheet(object):

    def __init__(self, file):
        self.sprites = pygame.image.load(file).convert_alpha()

    def extractSprite(self, x, y, width = 16, height = 16):
        image = pygame.Surface((width, height))
        image.fill((221, 229, 235)) # arbitrary color
        image.set_colorkey((221, 229, 235))
        imageRect = (x, y, width, height)
        image.blit(self.sprites, (0,0), imageRect)
        return image

    def extractSpriteGrid(self, coordinates, width = 16, height = 16, margin = 0):
        row, col = coordinates
        x = (col + margin) + (col * width)
        y = (row + margin) + (row * height)
        return self.extractSprite(x, y, width, height)


####################################
# UTILITY FUNCTIONS
####################################


def getCellCorner(data, row, col):
    return (data.MARGIN + data.GRID_SIZE * row, 
        data.MARGIN + data.GRID_SIZE * col)

def getCell(data, x, y):
    if(x < data.MARGIN or x > data.width or 
        y < data.MARGIN or y > data.height):
        return None
    else:
        return ((x - data.MARGIN) // data.GRID_SIZE + data.xOffsetEditor, 
            (y - data.MARGIN) // data.GRID_SIZE + data.yOffsetEditor)

def getOnscreenCell(data, x, y):
    if(x < data.MARGIN or x > data.width or 
        y < data.MARGIN or y > data.height):
        return None
    else:
        return ((x - data.MARGIN) // data.GRID_SIZE, 
            (y - data.MARGIN) // data.GRID_SIZE)


def getPlayCellCorner(data, row, col):
    return (data.PLAY_GRID_SIZE * (col - data.xOffsetPlay), 
        data.PLAY_GRID_SIZE * (row - data.yOffsetPlay))

def getPlayCell(data, x, y):
    if(x < 0 or x > data.width or y < 0 or y > data.height):
        return None
    else:
        # return (x // data.PLAY_GRID_SIZE + data.xOffsetPlay, 
        #     y // data.PLAY_GRID_SIZE + data.yOffsetPlay)
        return (y // data.PLAY_GRID_SIZE + data.yOffsetPlay, 
            x // data.PLAY_GRID_SIZE + data.xOffsetPlay)

def getPlayOnscreenCell(data, x, y):
    if(x < 0 or x > data.width or y < 0 or y > data.height):
        return None
    else:
        return (x // data.PLAY_GRID_SIZE, y // data.PLAY_GRID_SIZE)
