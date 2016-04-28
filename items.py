import pygame
from pygame.locals import *

import utilities as utils

class Item(pygame.sprite.Sprite):

    def getSprite(spriteCoords, size):
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        image = TILE_SPRITES.extractSpriteGrid(spriteCoords)
        image = pygame.transform.scale(image, (size, size))
        return image

    def __init__(self, row, col, data, spriteCoords):
        super().__init__()

        self.x, self.y = utils.getPlayCellCorner(data, row, col)
        self.offsetX, self.offsetY = self.x, self.y

        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        self.image = TILE_SPRITES.extractSpriteGrid(spriteCoords)
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def isOnBlock(self, data):
        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        if(blockCollisions != []):
            for entity in blockCollisions:
                if(self.rect.bottom + 2 > entity.rect.top):
                    self.rect.bottom = entity.rect.top
                    return True
        return False

    def update(self, data):
        if(data.xOffsetPlayPix > 0):
            self.offsetX = self.x - data.xOffsetPlayPix
        else:
            self.offsetX = self.x
        if(data.yOffsetPlayPix > 0):
            self.offsetY = self.y - data.yOffsetPlayPix
        else:
            self.offsetY = self.y

        self.rect.x, self.rect.y = self.offsetX, self.offsetY

class Shell(Item):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        image = TILE_SPRITES.extractSprite(78, 213, 16, 16)
        return pygame.transform.scale(image, (size, size))

    def __init__(self, row, col, data):
        super().__init__(row, col, data, (0, 0))
        self.active = False
        self.vx, self.vy = 0, 0
        self.COLLISION_MARGIN = 2
        self.held = False

        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        self.image = TILE_SPRITES.extractSprite(78, 213, 16, 16)
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y


    def setActive(self, throwDir):
        self.active = True
        self.vx = 6 if throwDir == "right" else -6

    def stopActive(self):
        self.active = False
        self.vx, self.vy = 0, 0

    def grabbed(self, data, direction):
        self.held = True
        if(direction == "left"):
            self.rect.left = data.player.rect.right
        elif(direction == "right"):
            self.rect.right = data.player.rect.left

    def update(self, data):
        if(self.held):
            self.vx, self.vy = 0, 0
            if(data.player.faceDir == "left"):
                self.rect.right = data.player.rect.left
            elif(data.player.faceDir == "right"):
                self.rect.left = data.player.rect.right
        else:
            self.x += self.vx
            self.y += self.vy

            self.top, self.bottom = self.rect.midtop, self.rect.midbottom
            self.left, self.right = self.rect.midleft, self.rect.midright

            self.blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
            self.enemyCollisions = pygame.sprite.spritecollide(self, data.enemyGroup, False)

            self.testBlockCollisions(data)
            self.testEnemyCollisions(data)

        self.rect.x, self.rect.y = self.x, self.y
        super().update(data)

    def testBlockCollisions(self, data):
        if(self.blockCollisions != []):
            for entity in self.blockCollisions:
                if(entity.rect.collidepoint((self.bottom[0], self.bottom[1] + self.COLLISION_MARGIN))):
                    # item above collided entity
                    self.vy = 0
                    self.rect.bottom = entity.rect.top - self.COLLISION_MARGIN
                elif(entity.rect.collidepoint((self.top[0], self.top[1] - self.COLLISION_MARGIN))):
                    #item below collided entity, should never happen
                    self.vy = 0
                    self.rect.top = entity.rect.bottom + self.COLLISION_MARGIN

        if(self.blockCollisions != []):
            for entity in self.blockCollisions:
                if((entity.rect.collidepoint((self.right[0] + self.COLLISION_MARGIN, self.right[1])))):
                    # item left of collided entity
                    self.vx = -1 * self.vx
                    self.rect.right = entity.rect.left - self.COLLISION_MARGIN
                elif(entity.rect.collidepoint((self.left[0] - self.COLLISION_MARGIN, self.left[1]))):
                    #item right of collided entity
                    self.vx =  -1 * self.vx
                    self.rect.left = entity.rect.right + self.COLLISION_MARGIN

    def testEnemyCollisions(self, data):
        if(self.enemyCollisions != []):
            for entity in self.enemyCollisions:
                if((entity.rect.collidepoint((self.right[0] + self.COLLISION_MARGIN, self.right[1])))):
                    # item left of collided entity
                    self.vy = 0
                    entity.deathSequence(data)
                elif(entity.rect.collidepoint((self.left[0] - self.COLLISION_MARGIN, self.left[1]))):
                    #item right of collided entity
                    self.vy = 0
                    entity.deathSequence(data)

        if(self.enemyCollisions != []):
            for entity in self.enemyCollisions:
                if(entity.rect.collidepoint((self.bottom[0] + self.COLLISION_MARGIN, self.bottom[1]))):
                    # item above collided entity
                    self.vy = -1 * self.vy
                    self.rect.bottom = entity.rect.top - self.COLLISION_MARGIN
                    entity.deathSequence(data)
                elif(entity.rect.collidepoint((self.top[0] - self.COLLISION_MARGIN, self.top[1]))):
                    #item below collided entity
                    self.vy = -1 * self.vx
                    self.rect.top = entity.rect.bottom - self.COLLISION_MARGIN
                    entity.deathSequence(data)

class RedShell(Shell):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        image = TILE_SPRITES.extractSprite(2, 213, 16, 16)
        return pygame.transform.scale(image, (size, size))

    def __init__(self, row, col, data):
        super().__init__(row, col, data)

        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        self.image = TILE_SPRITES.extractSprite(2, 213, 16, 16)
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        print(row, col)


class Mushroom(Item):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        image = TILE_SPRITES.extractSpriteGrid((0, 0))
        return pygame.transform.scale(image, (size, size))

    def __init__(self, row, col, data, spriteCoords, x = None, y = None):
        super().__init__(row, col, data, spriteCoords)
        if(x != None and y != None):
            self.x, self.y = x, y
            self.rect.x, self.rect.y = self.x, self.y

        self.vx, self.vy = -3, 0

        self.faceDir = "left"

        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        if(blockCollisions == []):
            self.vx = 0

    def update(self, data):
        self.rect.y += 2
        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        self.rect.y -= 2
        if(blockCollisions != []):
            self.vx = -3 if self.faceDir == "left" else 3

        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        if(blockCollisions != [] and self.vy > 0):
            self.vy = 0
            self.vx = -3
            self.rect.bottom = blockCollisions[0].rect.top
        else:
            self.rect.y -= 5
            blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
            if(blockCollisions != [] and self.vy == 0 and self.vx != 0):
                self.vx = -3 if self.faceDir == "left" else 3
                self.rect.y += 5
                if(self.vx < 0):
                    self.rect.left = blockCollisions[0].rect.right + 2
                elif(self.vx > 0):
                    self.rect.right = blockCollisions[0].rect.left - 2
                self.vx *= -1
                self.faceDir = "right" if self.faceDir == "left" else "left"
            else:
                self.rect.y += 5
                self.rect.y += 2
                blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
                if(blockCollisions == []):
                    if(self.vy == 0):
                        self.vy = 1
                    else:
                        self.vy += data.gravity
                self.rect.y -= 2


        #     if(self.vy == 0):
        #         print('a')
        #         self.vy = 1
        #     else:
        #         print('b')
        #         self.vy += data.gravity
        # # elif(self.isOnBlock(data)):
        #     print('c')
        #     blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        #     self.vy = 0
        #     self.rect.bottom = blockCollisions[0].rect.top

        self.x, self.y = self.rect.x, self.rect.y

        self.x += self.vx
        self.y += self.vy
        self.rect.x, self.rect.y = self.x, self.y

        super().update(data)


class FireFlower(Item):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        image = TILE_SPRITES.extractSprite(39, 1, 16, 15)
        return pygame.transform.scale(image, (size, size))

    def __init__(self, row, col, data, spriteCoords, x = None, y = None):
        super().__init__(row, col, data, spriteCoords)
        TILE_SPRITES = utils.SpriteSheet("images/newitems.png")
        self.image = TILE_SPRITES.extractSprite(39, 1, 16, 15)
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE, 
            data.PLAY_GRID_SIZE))
        if(x != None and y != None):
            self.x, self.y = x, y
            self.rect.x, self.rect.y = self.x, self.y

        self.vx, self.vy = 0, 0
