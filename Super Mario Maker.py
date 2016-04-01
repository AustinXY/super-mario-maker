import pygame
from pygame.locals import *

import random

import enemies
import level
import utilities as util

def init(data):
    data.mode = "designer"
    initEditor(data)

def initEditor(data):
    data.MARGIN = 100
    data.GRID_SIZE =  (data.width - data.MARGIN) // 18 # pixels
    
    data.GRID_HEIGHT, data.GRID_WIDTH = 10, 18
    data.LEVEL_HEIGHT, data.LEVEL_WIDTH = 27, 270

    data.level = level.Level("SMW")
    data.levelX = 17 # since height is 27 (indexed at 26) and height is 10
    data.xOffset = 0
    data.yOffset = 0


def keyPressed(event, data):
    pass

def mousePressed(event, data):
    pass

def timerFired(time, data):
    pass

def controller(data):
    for event in pygame.event.get():
        if(event.type == QUIT): return False
        elif(event.type == KEYDOWN):
            keyPressed(event, data)
        elif(event.type == MOUSEBUTTONDOWN):
            mousePressed(event, data)

def draw(data):
    if(data.mode == "mainMenu"):
        drawMenu(data)
    elif(data.mode == "designer"):
        drawDesigner(data)
    elif(data.mode == "play"):
        drawPlay(data)
    elif(data.mode == "online"):
        drawOnline(data)

def drawMenu(data):
    pass

def drawDesigner(data):
    drawGrid(data)

def drawGrid(data):
    # squares = list()
    # for row in range(data.GRID_HEIGHT):
    #     for col in range(data.GRID_WIDTH):
    #         squares.append(pygame.Rect(data.MARGIN + col * data.GRID_SIZE, data.MARGIN + row * data.GRID_SIZE, data.GRID_SIZE, data.GRID_SIZE))
    # for square in squares:
    #     pygame.draw.rect(data.screen, 0x000000, square, 1)
    
    pairs = list()
    for row in range(data.GRID_HEIGHT):
        pairs.append(((data.MARGIN, data.MARGIN + row * data.GRID_SIZE), (data.width, data.MARGIN + row * data.GRID_SIZE)))
    for col in range(data.GRID_WIDTH):
        pairs.append(((data.MARGIN + col * data.GRID_SIZE, data.MARGIN), (data.MARGIN + col * data.GRID_SIZE, data.height)))
    # pairs.append(((data.width - 2, data.MARGIN), (data.width - 2, data.height)))
    # pairs.append(((data.MARGIN, data.height - 2), (data.width, data.height - 2)))
    for pair in pairs:
        pygame.draw.line(data.screen, 0x000000, pair[0], pair[1])
    # pygame.draw.line(data.screen, 0x000000, (data.width - 1, data.MARGIN), (data.width - 1, data.height), 2)
    # pygame.draw.line(data.screen, 0x000000, (data.MARGIN, data.height - 1), (data.width, data.height - 1), 2)

    pygame.display.flip()

def drawPlay(data):
    pass

def drawOnline(data):
    pass




def run(width = 1000, height = 600):
    pygame.init()
    clock = pygame.time.Clock()

    class Struct(object): pass
    data = Struct()
    data.width, data.height = width, height
    init(data)

    data.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Super Mario Maker")
    data.screen.fill((255, 255, 255))
    pygame.display.flip()

    while(True):
        time = clock.tick(60) # frames per second
        timerFired(data, time)
        if(controller(data) == False): return
        draw(data)

run(1000, 600)