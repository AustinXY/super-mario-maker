import pygame
from pygame.locals import *

import random

import items
import utilities as utils

class Background(pygame.sprite.Sprite):

    def __init__(self, data, spriteCoords):
        super().__init__()
        TILE_SPRITES = utils.SpriteSheet("images/backgrounds.png")

        self.x, self.y = 0, 0

        self.image = pygame.Surface((data.width, data.height))

        coord = random.choice([(0, 0), (1, 1), (3, 0)])
        
        self.bg = TILE_SPRITES.extractSpriteGrid((0, 0), 512, 432, 2)
        self.bg = pygame.transform.scale(self.bg, (711, data.height))
        self.bgW, self.bgH = self.bg.get_width(), self.bg.get_height()

        x = 0
        while (x < data.width):
            self.image.blit(self.bg, (x, 0, self.bgW, self.bgH))
            x += self.bgW

        self.rect = self.image.get_rect()

    def update(self, data):
        # parallax scrolling wheeeeeeeee
        x = 0 - (.2 * data.xOffsetPlayPix)
        while (x < data.width):
            self.image.blit(self.bg, (x, 0, self.bgW, self.bgH))
            x += self.bgW

        self.rect = self.image.get_rect()


class Block(pygame.sprite.Sprite):

    @staticmethod
    def getSprite(width, height, spriteCoords):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid(spriteCoords)
        image = pygame.transform.scale(image, (width, height))
        return image

    def __init__(self, data, row, col, spriteCoords, rootBlock = True):
        super().__init__()
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")

        self.x, self.y = utils.getPlayCellCorner(data, row, col)
        self.offsetX, self.offsetY = self.x, self.y

        if(rootBlock):
            topLevel = (6, 2)
            interLevel = (7, 2)
            if(data.level.getMap()[row - 1][col] != "block"):
                spriteCoords = topLevel
            else:
                spriteCoords = interLevel
        
        self.image = TILE_SPRITES.extractSpriteGrid(spriteCoords)
        self.image = pygame.transform.scale(self.image, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def update(self, data):
        if(data.xOffsetPlayPix > 0):
            self.offsetX = self.x - data.xOffsetPlayPix
        if(data.yOffsetPlayPix > 0):
            self.offsetY = self.y - data.yOffsetPlayPix

        self.rect.x, self.rect.y = self.offsetX, self.offsetY

class Brick(Block):

    def __init__(self, data, row, col, spriteCoords):
        super().__init__(data, row, col, spriteCoords, False)

        self.spinning = False
        self.ticks = 0

        self.standingImage = self.image

        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        self.spin1 = TILE_SPRITES.extractSpriteGrid((0, 2))
        self.spin1  =pygame.transform.scale(self.spin1, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.spin2 = TILE_SPRITES.extractSpriteGrid((0, 3))
        self.spin2 = pygame.transform.scale(self.spin2, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.spin3 = TILE_SPRITES.extractSpriteGrid((0, 4))
        self.spin3 = pygame.transform.scale(self.spin3, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.spinningSprites = [self.spin1, self.spin2, self.spin3]

    def spin(self):
        self.spinning = True

    def update(self, data):
        if(self.spinning):
            if(self.ticks < 60):
                ticks = self.ticks //3
                self.image = self.spinningSprites[ticks % 3]
                self.ticks += 1
            else:
                self.image = self.standingImage
                self.spinning = False
                self.ticks = 0

        super().update(data)


class Question(Block):

    def __init__(self, data, row, col, spriteCoords, item = "coin"):
        super().__init__(data, row, col, spriteCoords, False)
        self.row, self.col = row, col
        self.item = item

        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid((3, 0))
        self.hitImage = pygame.transform.scale(image, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))

    def spawnItem(self, data):
        if(self.item == "coin"):
            data.coins += 1
            self.item = None
        elif(self.item != None):
            self.itemx, self.itemy = utils.getPlayCellCorner(data, self.row - 1, self.col)
            if(self.item == "mushroom"):
                data.spawnitemSFX.play()

                data.itemGroup.add(items.Mushroom(self.row - 1, 
                    self.col, data, data.mushroomSpritePos))

            elif(self.item == "flower"):
                data.spawnitemSFX.play()

                data.itemGroup.add(items.FireFlower(self.row - 1, 
                    self.col, data, data.mushroomSpritePos))

            self.item = None

        self.image = self.hitImage

    def getItem(self):
        return self.item



class Kaizo(Question):

    @staticmethod
    def getSprite(width, height, spriteCoords):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid(spriteCoords)
        image = pygame.transform.scale(image, (width, height))

        transLayer = pygame.image.load("images/transparent.png").convert_alpha()
        transLayer = pygame.transform.scale(transLayer, (width, height))

        image.blit(transLayer, (0, 0))
        return image

    def __init__(self, data, row, col, spriteCoords):
        super().__init__(data, row, col, spriteCoords, False)

        width, height = self.image.get_width(), self.image.get_height()
        self.image = pygame.Surface((width, height))
        self.image.fill(data.WHITE)
        self.image.set_colorkey(data.WHITE)



class Platform(Block):

    @staticmethod
    def getSprite(width, height, spriteCoords):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid(spriteCoords[1])
        return pygame.transform.scale(image, (width, height))

    @staticmethod
    def getFullSprite(height, spriteCoords):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image1 = TILE_SPRITES.extractSpriteGrid(spriteCoords[0])
        image2 = TILE_SPRITES.extractSpriteGrid(spriteCoords[1])
        image3 = TILE_SPRITES.extractSpriteGrid(spriteCoords[2])

        image = pygame.Surface((image1.get_width() + 
            image2.get_width() + image3.get_width(), 
            image1.get_height()))

        image.fill((221, 229, 235)) # arbitrary color
        image.set_colorkey((221, 229, 235))

        image.blit(image1, (0, 0))
        image.blit(image2, (image1.get_width(), 0))
        image.blit(image3, (image1.get_width() + image2.get_width(), 0))

        return pygame.transform.scale(image, (height * 3, height))


    def __init__(self, data, row, col, spriteCoords):
        super().__init__(data, row, col, (0, 0), False)
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")

        self.x, self.y = utils.getPlayCellCorner(data, row - 1, col)
        self.offsetX, self.offsetY = self.x, self.y
        
        self.image1 = TILE_SPRITES.extractSpriteGrid(spriteCoords[0])
        self.image2 = TILE_SPRITES.extractSpriteGrid(spriteCoords[1])
        self.image3 = TILE_SPRITES.extractSpriteGrid(spriteCoords[2])

        self.image = pygame.Surface((self.image1.get_width() + 
            self.image2.get_width() + self.image3.get_width(), 
            self.image1.get_height()))

        self.image.fill((221, 229, 235)) # arbitrary color
        self.image.set_colorkey((221, 229, 235))

        self.image.blit(self.image1, (0, 0))
        self.image.blit(self.image2, (self.image1.get_width(), 0))
        self.image.blit(self.image3, 
            (self.image1.get_width() + self.image2.get_width(), 0))

        self.image = pygame.transform.scale(self.image, 
            (data.PLAY_GRID_SIZE * 3, data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

class FallingPlatform(Platform):

    def __init__(self, data, row, col, spriteCoords):
        super().__init__(data, row, col, spriteCoords)
        self.falling = False
        self.vx, self.vy = 0, 0

    def activate(self, data):
        self.falling = True
        self.vy = 5

    def update(self, data):
        if(self.falling):
            self.y += self.vy
            self.vy += data.gravity
            self.rect.x, self.rect.y = self.x, self.y

        super().update(data)

class Spike(Block):

    @staticmethod
    def getSprite(size):
        image = pygame.image.load("images/spikes.png").convert_alpha()
        return pygame.transform.scale(image, (size, size))

    def __init__(self, data, row, col, spriteCoords):
        super().__init__(data, row, col, spriteCoords, False)

        self.x, self.y = utils.getPlayCellCorner(data, row, col)
        
        self.image = pygame.image.load("images/spikes.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE, 
            data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        # super().__init__(data, row, col, spriteCoords)
        
class Pipe(Block):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid((3, 4))
        image = pygame.transform.scale(image, (size, size))
        return image

    @staticmethod
    def getPipeBody(size):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid((4, 4))
        image = pygame.transform.scale(image, (size, size))
        return image

    @staticmethod
    def getUpsideDownPipe(size):
        TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
        image = TILE_SPRITES.extractSpriteGrid((5, 4))
        image = pygame.transform.scale(image, (size, size))
        return image        


    def __init__(self, data, row, col, spriteCoords, pipeKey):
        super().__init__(data, row, col, spriteCoords, False)
        if(data.level.getMap()[row - 1][col] == "block"):
            TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
            self.image = TILE_SPRITES.extractSpriteGrid((5, 4))
            self.image = pygame.transform.scale(self.image, 
                (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))

        if(data.level.getMap()[row - 1][col] == "pipe"):
            TILE_SPRITES = utils.SpriteSheet("images/blocktiles.png")
            self.image = TILE_SPRITES.extractSpriteGrid((4, 4))
            self.image = pygame.transform.scale(self.image, 
                (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))

        self.pipeKey = pipeKey

class EndPole(Block):

    @staticmethod
    def getSprite(size):
        image = pygame.image.load("images/gate.png").convert_alpha()
        width, height = image.get_width(), image.get_height()
        image = pygame.transform.scale(image, (size, int(height / width * size)))
        return image

    @staticmethod
    def getSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))

        image = pygame.image.load("images/gate.png").convert_alpha()
        width, height = image.get_width(), image.get_height()
        image = pygame.transform.scale(image, (int(width / height * size), size))
        return image

    def __init__(self, data, row, col):
        super().__init__(data, row - 2, col, (0, 0), False)
        self.image = pygame.image.load("images/gate.png").convert_alpha()
        width, height = self.image.get_width(), self.image.get_height()
        self.image = pygame.transform.scale(self.image, 
            (int(width / height * 3 *data.PLAY_GRID_SIZE), 3 * data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        # width, height = pygame.