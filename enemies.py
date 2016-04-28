import pygame
from pygame.locals import *

import math

import utilities as utils
import items

class Enemy(pygame.sprite.Sprite):

    def __init__(self, row, col, faceDir, data):
        super().__init__()
        self.x, self.y = utils.getPlayCellCorner(data, row, col)
        self.offsetX, self.offsetY = self.x, self.y

        self.vy = 0

        self.image = pygame.Surface((data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.faceDir = faceDir
        self.frontTest = 5 # pixels

        self.ticks = 0

        self.rect.y -= 5
        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        self.rect.y += 5
        if(blockCollisions == []):
            self.vx = 0
        else:
            self.vx = -3


    def update(self, data):
        self.x += self.vx
        self.y += self.vy
        
        if(data.xOffsetPlayPix > 0 or data.yOffsetPlayPix > 0):
            if(data.xOffsetPlayPix > 0):
                self.offsetX = self.x - data.xOffsetPlayPix
            if(data.yOffsetPlayPix > 0):
                self.offsetY = self.y - data.yOffsetPlayPix
        else:
            self.offsetX, self.offsetY = self.x, self.y
        
        self.rect.x, self.rect.y = self.offsetX, self.offsetY

        if(self.vx != 0):
            self.ticks += 1
        else:
            self.ticks = 0

    def deathSequence(self, data):
        self.kill()

class Goomba(Enemy):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image1 = TILE_SPRITES.extractSprite(191, 237, 16, 16)
        return pygame.transform.scale(image1, (size, size))

    def __init__(self, row, col, winged, faceDir, data):
        super().__init__(row, col, faceDir, data)

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.image1 = TILE_SPRITES.extractSprite(191, 237, 16, 16)
        self.image1 = pygame.transform.scale(self.image1, 
            (int(data.PLAY_GRID_SIZE ), data.PLAY_GRID_SIZE))

        self.image2 = TILE_SPRITES.extractSprite(172, 238, 16, 15)
        self.image2 = pygame.transform.scale(self.image2, 
            (int(data.PLAY_GRID_SIZE), data.PLAY_GRID_SIZE))
        self.leftSprites = [self.image1, self.image2]

        self.rightSprites = list()
        for sprite in self.leftSprites:
            self.rightSprites.append(pygame.transform.flip(sprite, True, False))

        self.winged = winged
        self.jumpable = True

    def update(self, data):
        self.setImage()

        # blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        # if(blockCollisions != [] and self.vy > 0):
        #     self.vy = 0
        #     self.vx = -3
        #     self.rect.bottom = blockCollisions[0].rect.top
        # else:
        #     self.rect.y -= 5
        #     blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        #     self.rect.y += 5
        #     blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        #     if(blockCollisions == []):
        #         if(self.vy == 0):
        #             self.vy = 1
        #         else:
        #             self.vy += data.gravity

        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        if(blockCollisions != [] and self.vy > 0):
            self.vy = 0
            self.vx = -3
            self.rect.bottom = blockCollisions[0].rect.top
        else:
            self.rect.y += 2
            blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
            self.rect.y -= 2
            if(blockCollisions != []):
                self.vx = -3 if self.faceDir == "left" else 3

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
                blockCollisions = pygame.sprite.spritecollide(self, 
                    data.platformGroup, False)
                if(blockCollisions == []):
                    if(self.vy == 0):
                        self.vy = 1
                    else:
                        self.vy += data.gravity
                self.rect.y -= 2

        super().update(data)

    def setImage(self):
        if(self.faceDir == "left"):
            if(self.vx == 0 or self.vy != 0):
                self.image = self.leftSprites[0]
            elif(self.vx <= 0 ):
                self.image = self.leftSprites[self.ticks // 2 % 2]
        elif(self.faceDir == "right"):
            if(self.vx == 0) or self.vy != 0:
                self.image = self.rightSprites[0]
            elif(self.vx >= 0 ):
                self.image = self.rightSprites[self.ticks // 2 % 2]


        temprect = self.image.get_rect()
        temprect.x, temprect.y = self.offsetX, self.offsetY
        self.rect = temprect


class Koopa(Enemy):
    
    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(21, 3, 16, 27)
        image =  pygame.transform.scale(image1, (int(size * 16 / 27), size))
        return pygame.transform.flip(image, True, False)

    @staticmethod
    def getSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(21, 3, 16, 27)
        image = pygame.transform.scale(image, (int(size * 16 / 27), size))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        
        return pygame.transform.flip(surface, True, False)

    def __init__(self, row, col, winged, faceDir, data):
        super().__init__(row, col, faceDir, data)

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.image1 = TILE_SPRITES.extractSprite(3, 3, 16, 27)
        self.image1 = pygame.transform.scale(self.image1, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.image2 = TILE_SPRITES.extractSprite(21, 3, 16, 27)
        self.image2 = pygame.transform.scale(self.image2, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.image3 = TILE_SPRITES.extractSprite(40, 3, 16, 27)
        self.image3 = pygame.transform.scale(self.image3, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.rightSprites = [self.image1, self.image2, self.image3]

        self.leftSprites = list()
        for sprite in self.rightSprites:
            self.leftSprites.append(pygame.transform.flip(sprite, True, False))
        
        self.winged = winged
        self.jumpable = True

    def update(self, data):
        self.setImage()

        # blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        # if(blockCollisions != [] and self.vy > 0):
        #     self.vy = 0
        #     self.vx = -3
        #     self.rect.bottom = blockCollisions[0].rect.top
        # else:
        #     self.rect.y -= 5
        #     blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        #     self.rect.y += 5
        #     if(blockCollisions == []):
        #         if(self.vy == 0):
        #             self.vy = 1
        #         else:
        #             self.vy += data.gravity

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

        super().update(data)

    def setImage(self):
        if(self.faceDir == "left"):
            if(self.vx == 0 or self.vy != 0):
                self.image = self.leftSprites[1]
            elif(self.vx <= 0 ):
                self.image = self.leftSprites[self.ticks // 2 % 3]
        elif(self.faceDir == "right"):
            if(self.vx == 0 or self.vy != 0):
                self.image = self.rightSprites[1]
            elif(self.vx >= 0 ):
                self.image = self.rightSprites[self.ticks // 2 % 3]

        temprect = self.image.get_rect()
        temprect.x, temprect.y = self.offsetX, self.offsetY
        self.rect = temprect

    def deathSequence(self, data):
        row, col = utils.getPlayCell(data, self.x, self.y)
        data.itemGroup.add(items.Shell(row, col, data))
        super().deathSequence(data)

class RedKoopa(Koopa):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(21, 39, 16, 27)
        image =  pygame.transform.scale(image1, (int(size * 16 / 27), size))
        return pygame.transform.flip(image, True, False)

    @staticmethod
    def getSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(21, 39, 16, 27)
        image = pygame.transform.scale(image, (int(size * 16 / 27), size))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        
        return pygame.transform.flip(surface, True, False)
    
    def __init__(self, row, col, winged, faceDir, data):
        super().__init__(row, col, False, faceDir, data)

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.image1 = TILE_SPRITES.extractSprite(3, 39, 16, 27)
        self.image1 = pygame.transform.scale(self.image1, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.image2 = TILE_SPRITES.extractSprite(21, 39, 16, 27)
        self.image2 = pygame.transform.scale(self.image2, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.image3 = TILE_SPRITES.extractSprite(40, 39, 16, 27)
        self.image3 = pygame.transform.scale(self.image3, 
            (int(data.PLAY_GRID_SIZE * 16 / 27), data.PLAY_GRID_SIZE))

        self.rightSprites = [self.image1, self.image2, self.image3]

        self.leftSprites = list()
        for sprite in self.rightSprites:
            self.leftSprites.append(pygame.transform.flip(sprite, True, False))

        self.winged = winged
        self.jumpable = True

    def update(self, data):
        self.rect.y += 5
        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        self.rect.y -= 5
        if(blockCollisions == []):
            air = True
        else:
            air =False

        print(air)
        if(self.faceDir == "left" and self.vy == 0 and not air):
            emptyFront = True
            self.frontX = self.rect.left - self.frontTest
            self.frontY = self.rect.bottom + self.frontTest
            for entity in data.platformGroup:
                if(entity.rect.collidepoint(self.frontX, self.frontY)):
                    emptyFront = False
            if(emptyFront):
                self.faceDir = "right"
                self.vx *= -1
        elif(self.faceDir == "right" and self.vy == 0 and not air):
            emptyFront = True
            self.frontX = self.rect.left + self.frontTest
            self.frontY = self.rect.bottom + self.frontTest
            for entity in data.platformGroup:
                if(entity.rect.collidepoint(self.frontX, self.frontY)):
                    emptyFront = False
            if(emptyFront):
                self.faceDir = "left"
                self.vx *= -1
        super().update(data)

    def deathSequence(self, data):
        row, col = utils.getPlayCell(data, self.x, self.y)
        data.itemGroup.add(items.RedShell(row, col, data))
        self.kill()



class Blaster(Enemy):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        image = TILE_SPRITES.extractSprite(65, 40, 15, 17)
        return pygame.transform.scale(image, (size, int(17 / 15 * size)))


    def __init__(self, row, col, faceDir, data):
        super().__init__(row, col, faceDir, data)

        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        self.image = TILE_SPRITES.extractSprite(65, 40, 15, 17)
        self.image = pygame.transform.scale(self.image, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.row, self.col = row, col
        self.jumpable = False
        self.vx, self.vy = 0, 0
        self.fireTicks = 0
        self.tolerance = 500

    def update(self, data):
        if(0 < self.rect.left - data.player.rect.right <= self.tolerance):
            if(self.fireTicks % 60 == 0):
                data.enemyGroup.add(CannonBall(self.row, self.col, "left", 
                    data, self.x, self.y))
            self.fireTicks += 1
        # elif(0 < data.player.rect.left - self.rect.right <= self.tolerance):
        #     if(self.fireTicks % 60 == 0):
        #         data.enemyGroup.add(CannonBall(self.row, self.col, "right", 
        #             data, self.x, self.y))
        #     self.fireTicks += 1
        else:
            self.fireTicks = 0

        super().update(data)



class CannonBall(Enemy):

    def __init__(self, row, col, faceDir, data, x, y):
        super().__init__(row, col, faceDir, data)
        
        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        self.rightImage = TILE_SPRITES.extractSprite(56, 23, 12, 12)
        self.rightImage = pygame.transform.scale(self.rightImage, 
            (int(data.PLAY_GRID_SIZE * .8), int(data.PLAY_GRID_SIZE * .8)))

        self.leftImage = pygame.transform.flip(self.rightImage, True, False)
        self.leftImage = pygame.transform.scale(self.leftImage, 
            (int(data.PLAY_GRID_SIZE * .8), int(data.PLAY_GRID_SIZE * .8)))

        self.image = self.leftImage

        self.jumpable = True

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.vx = -4 if(self.faceDir == "left") else 4
        self.vy = -4

    def update(self, data):
        if(self.vx < 0):
            self.image = self.leftImage
        else:
            self.image = self.rightImage
        super().update(data)

class BulletShooter(Enemy):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        image = TILE_SPRITES.extractSprite(0, 20, 16, 33)
        return pygame.transform.scale(image, (int(16 / 33 * size), size))

    @staticmethod
    def getSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))

        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        image = TILE_SPRITES.extractSprite(0, 20, 16, 33)
        image = pygame.transform.scale(image, (int(16 / 33 * size), size))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        return surface

        

    def __init__(self, row, col, faceDir, data):
        super().__init__(row, col, faceDir, data)

        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        self.image = TILE_SPRITES.extractSprite(0, 20, 16, 33)
        self.image = pygame.transform.scale(self.image, 
            (int(16 / 33 * data.PLAY_GRID_SIZE), data.PLAY_GRID_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.row, self.col = row, col
        self.jumpable = False
        self.vx, self.vy = 0, 0
        self.fireTicks = 0
        self.tolerance = 500

    def update(self, data):
        # print(self.x, self.y, "bullet")

        if(0 <= self.rect.left - data.player.rect.right <= self.tolerance):
            if(self.fireTicks % 60 == 0):
                data.enemyGroup.add(Bullet(self.row, self.col, "left", 
                    data, self.x, self.y))
            self.fireTicks += 1
        elif(0 <= data.player.rect.left - self.rect.right <= self.tolerance):
            if(self.fireTicks % 60 == 0):
                data.enemyGroup.add(Bullet(self.row, self.col, "right", 
                    data, self.x, self.y))
            self.fireTicks += 1
        else:
            print("wtf fam")
            self.fireTicks = 0

        super().update(data)

class Bullet(CannonBall):

    def __init__(self, row, col, faceDir, data, x, y):
        super().__init__(row, col, faceDir, data, x, y)

        TILE_SPRITES = utils.SpriteSheet("images/cannons.png")
        self.rightImage = TILE_SPRITES.extractSprite(36, 21, 16, 14)
        self.leftImage = pygame.transform.flip(self.rightImage, True, False)
        self.image = self.leftImage

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.vx = -5 if faceDir == "left" else 5
        self.vy = 0


class Thwomp(Enemy):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image1 = TILE_SPRITES.extractSprite(211, 358, 24, 32)
        return pygame.transform.scale(image1, (int(size * 24 / 32), size))

    @staticmethod
    def getSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(211, 358, 24, 32)
        image = pygame.transform.scale(image, (int(size * 24 / 32), size))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        
        return surface

    def __init__(self, row, col, data):
        super().__init__(row, col, "left", data)
        self.ogX, self.ogY = self.x, self.y

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.stillImage = TILE_SPRITES.extractSprite(211, 358, 24, 32)
        self.stillImage = pygame.transform.scale(self.stillImage, 
            (int(2 * data.PLAY_GRID_SIZE * 24 / 32), 2 * data.PLAY_GRID_SIZE))

        self.fallingImage = TILE_SPRITES.extractSprite(211, 397, 24, 32)
        self.fallingImage = pygame.transform.scale(self.fallingImage, 
            (int(2 * data.PLAY_GRID_SIZE * 24 / 32), 2 * data.PLAY_GRID_SIZE))

        self.risingImage = TILE_SPRITES.extractSprite(245, 358, 24, 32)
        self.risingImage = pygame.transform.scale(self.risingImage, 
            (int(2 * data.PLAY_GRID_SIZE * 24 / 32), 2 * data.PLAY_GRID_SIZE))

        self.sprites = [self.stillImage, self.fallingImage, self.risingImage]

        self.jumpable = False
        self.active = False
        self.fallingTicks = 0
        self.tolerance = 50
        self.falling = False

        self.sinceHitGround = 0

        self.rect = self.stillImage.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.vx, self.vy = 0, 0

    def update(self, data):
        print(self.fallingTicks)

        if(self.vy == 0):
            self.image = self.stillImage
        elif(self.vy > 0):
            self.image = self.fallingImage
        elif(self.vy < 0):
            self.image = self.risingImage

        if(self.fallingTicks == 0):
            if((abs(self.rect.left - data.player.rect.right) <= self.tolerance) or
                (abs(data.player.rect.left - self.rect.right) <= self.tolerance)):
                self.active = True
                self.falling = True
                self.fallingTicks += 1
                self.vy = 7

        if(self.fallingTicks > 0):
            if(self.fallingTicks < 20):
                self.fallingTicks += 1
            else:
                self.blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
                if(self.falling):
                    if(self.blockCollisions == []):
                        self.y += self.vy
                    else:
                        self.falling = False
                        self.sinceHitGround = 0
                        self.vy = 0
                        self.rect.bottom = self.blockCollisions[0].rect.top
                elif(not self.falling):
                    if(self.sinceHitGround < 30):
                        self.sinceHitGround += 1
                    else:
                        self.vy = -5
                        if(self.y <= self.ogY):
                            self.vy = 0
                            self.active = False
                            self.fallingTicks = 0
                            self.y = self.ogY

        super().update(data)



class Boo(Enemy):

    def __init__(self, row, col, faceDir, data):
        super().__init__(row, col, faceDir, data)
        self.jumpable = False

    def update(self, data):
        pass

class Fire(Enemy):

    @staticmethod
    def getSprite(size):
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        image = TILE_SPRITES.extractSprite(350, 173, 16, 16)
        return pygame.transform.scale(image, (size, size))


    def __init__(self, row, col, data):
        super().__init__(row, col, "left", data)
        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.image = TILE_SPRITES.extractSprite(350, 173, 16, 16)
        self.image = pygame.transform.scale(self.image, 
            (data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.upImage = self.image
        self.downImage = pygame.transform.flip(self.image, False, True)

        self.ogY = self.y

        self.vx = 0 
        self.vy = -40

        self.flameTicks = 0
        self.jumpable = False
        self.waiting = False

    def update(self, data):
        if(not self.waiting):
            if(self.vy >= 0):
                self.image = self.downImage
            elif(self.vy < 0):
                self.image = self.upImage
        else:
            width, height = self.image.get_width(), self.image.get_height()
            self.image = pygame.Surface((width, height))
            self.image.fill(data.WHITE)
            self.image.set_colorkey(data.WHITE)

        if(not self.waiting):
            if(self.vy == 0):
                self.vy = 5
                self.image = self.downImage
            elif(self.y > self.ogY):
                self.vy = 0
                self.y = self.ogY
                self.image = self.upImage
                self.waiting = True
            else:
                self.vy += 3
        elif(self.waiting):
            if(self.flameTicks > 20):
                self.vy = -40
                self.waiting = False
                self.flameTicks = 0
            else:
                self.flameTicks += 1


        super().update(data)