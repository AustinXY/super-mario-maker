import pygame
from pygame.locals import *

import enemies
import blocks
import items
import level
import utilities as utils


class Player(pygame.sprite.Sprite):

    # static methods below for getting just a single sprite image
    # used for representing player start in the editor mode

    @staticmethod
    def getSprite(height):
        TILE_SPRITES = utils.SpriteSheet("images/mario.png")
        image = TILE_SPRITES.extractSprite(4, 9, 14, 20)
        image = pygame.transform.scale(image, (int(height * 14 / 20), int(height)))
        return image

    @staticmethod
    def getSuperSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))
        TILE_SPRITES = utils.SpriteSheet("images/mario.png")
        image = TILE_SPRITES.extractSprite(5, 60, 13, 28)
        image = pygame.transform.scale(image, (int(size * 13 / 28), int(size)))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        
        return surface

    @staticmethod
    def getSmallSquareSprite(size):
        surface = pygame.Surface((size, size))
        surface.fill((221, 229, 235)) # arbitrary color
        surface.set_colorkey((221, 229, 235))
        TILE_SPRITES = utils.SpriteSheet("images/mario.png")
        image = TILE_SPRITES.extractSprite(4, 9, 14, 20)
        image = pygame.transform.scale(image, (int(size * 14 / 20), size))

        x = (size / 2) - image.get_width() / 2
        surface.blit(image, (x, 0))
        
        return surface

    def __init__(self, row, col, style, data):
        super().__init__()
        print(row, col)
        self.x, self.y = utils.getPlayCellCorner(data, row, col)
        self.absX, self.absY = self.x, self.y
        self.vx = 0
        self.vy = 0

        self.state = "small"
        self.living = True
        self.completed = False
        self.onPipe = False

        self.invul = False
        self.invulCount = 0

        self.grabbing = False
        self.held = None

        self.leftPressed = False
        self.rightPressed = False

        self.COLLISION_MARGIN = 0

        self.image = pygame.Surface((data.PLAY_GRID_SIZE, data.PLAY_GRID_SIZE))
        self.image.fill((255, 0, 0))

        self.initSmallAnimFrames(data)
        self.initSuperAnimFrames(data)
        self.initFireAnimFrames(data)

        self.width, self.height = self.image.get_size()
        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.tick = 0
        self.winTicks = 0
        self.deathTicks = 0

        self.faceDir = "right"

        self.decelerating = False
        print(self.rect)
        # self.updateValues()
        # self.rect.x, self.rect.y = self.x, self.y'

    def initSmallAnimFrames(self, data):
        # initialises all the sprites necessary to represent small Mario in
        # his states: moving left, right, jumping, and falling

        TILE_SPRITES = utils.SpriteSheet("images/mario.png")
        self.smallRightSprites = list()

        image = TILE_SPRITES.extractSprite(4, 9, 14, 20)
        self.smallRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 14 / 20), int(data.PLAY_GRID_SIZE * 0.9))))

        image = TILE_SPRITES.extractSprite(21, 9, 15, 19)
        self.smallRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 15 / 19), int(data.PLAY_GRID_SIZE * 0.9))))

        image = TILE_SPRITES.extractSprite(38, 9, 15, 20)
        self.smallRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 15 / 20), int(data.PLAY_GRID_SIZE * 0.9))))

        image = TILE_SPRITES.extractSprite(55, 9, 15, 19)
        self.smallRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 15 / 19), int(data.PLAY_GRID_SIZE * 0.9))))

        self.smallLeftSprites = list()
        for image in self.smallRightSprites:
            self.smallLeftSprites.append(pygame.transform.flip(image, True, False))

        self.smallRightJumpSprite = TILE_SPRITES.extractSprite(105, 6, 16, 22)
        self.smallRightJumpSprite = pygame.transform.scale(self.smallRightJumpSprite, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 16 / 22), int(data.PLAY_GRID_SIZE * 0.9)))

        self.smallLeftJumpSprite = pygame.transform.flip(self.smallRightJumpSprite, True, False)

        self.smallRightFallingSprite = TILE_SPRITES.extractSprite(123, 7, 15, 20)
        self.smallRightFallingSprite = pygame.transform.scale(self.smallRightFallingSprite, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 15 / 20), int(data.PLAY_GRID_SIZE * 0.9)))

        self.smallLeftFallingSprite = pygame.transform.flip(self.smallRightFallingSprite, True, False)

        self.smallVictory = TILE_SPRITES.extractSprite(241, 8, 16, 21)
        self.smallVictory = pygame.transform.scale(self.smallVictory, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 16 / 21), int(data.PLAY_GRID_SIZE * 0.9)))

        self.deadSprite = TILE_SPRITES.extractSprite(401, 6, 16, 24)
        self.deadSprite = pygame.transform.scale(self.deadSprite, 
            (int(data.PLAY_GRID_SIZE * 0.9 * 16 / 24), int(data.PLAY_GRID_SIZE * 0.9)))

    def initSuperAnimFrames(self, data):
        # initialises all the sprites necessary to represent super Mario in
        # his states: moving left, right, jumping, and falling

        TILE_SPRITES = utils.SpriteSheet("images/mario.png")
        self.superRightSprites = list()

        image = TILE_SPRITES.extractSprite(5, 60, 13, 28)
        self.superRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 13 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(22, 60, 15, 28)
        self.superRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 15 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(38, 61, 16, 26)
        self.superRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 26), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(56, 60, 15, 28)
        self.superRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 15 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(73, 60, 15, 28)
        self.superRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 15 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        self.superLeftSprites = list()
        for image in self.superRightSprites:
            self.superLeftSprites.append(pygame.transform.flip(image, True, False))

        self.superRightJumpSprite = TILE_SPRITES.extractSprite(145, 59, 16, 30)
        self.superRightJumpSprite = pygame.transform.scale(self.superRightJumpSprite, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 30), int(data.PLAY_GRID_SIZE * 1.25)))

        self.superLeftJumpSprite = pygame.transform.flip(self.superRightJumpSprite, True, False)

        self.superRightFallingSprite = TILE_SPRITES.extractSprite(168, 60, 16, 29)
        self.superRightFallingSprite = pygame.transform.scale(self.superRightFallingSprite, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 29), int(data.PLAY_GRID_SIZE * 1.25)))

        self.superLeftFallingSprite = pygame.transform.flip(self.superRightFallingSprite, True, False)

        self.superVictory = TILE_SPRITES.extractSprite(307, 63, 16, 28)
        self.superVictory = pygame.transform.scale(self.superVictory, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 29), int(data.PLAY_GRID_SIZE * 1.25)))

    def initFireAnimFrames(self, data):
        # initialises all the sprites necessary to represent super Mario in
        # his states: moving left, right, jumping, and falling

        TILE_SPRITES = utils.SpriteSheet("images/firemario.png")
        self.fireRightSprites = list()

        image = TILE_SPRITES.extractSprite(3, 3, 15, 28)
        self.fireRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 15 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(123, 3, 16, 27)
        self.fireRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 27), int(data.PLAY_GRID_SIZE * 1.25))))

        image = TILE_SPRITES.extractSprite(163, 3, 16, 28)
        self.fireRightSprites.append(pygame.transform.scale(image, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 28), int(data.PLAY_GRID_SIZE * 1.25))))

        self.fireLeftSprites = list()
        for image in self.fireRightSprites:
            self.fireLeftSprites.append(pygame.transform.flip(image, True, False))

        self.fireRightJumpSprite = TILE_SPRITES.extractSprite(3, 41, 16, 31)
        self.fireRightJumpSprite = pygame.transform.scale(self.fireRightJumpSprite, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 31), int(data.PLAY_GRID_SIZE * 1.25)))

        self.fireLeftJumpSprite = pygame.transform.flip(self.fireRightJumpSprite, True, False)

        self.fireRightFallingSprite = TILE_SPRITES.extractSprite(43, 42, 16, 29)
        self.fireRightFallingSprite = pygame.transform.scale(self.fireRightFallingSprite, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 29), int(data.PLAY_GRID_SIZE * 1.25)))

        self.fireLeftFallingSprite = pygame.transform.flip(self.fireRightFallingSprite, True, False)

        self.fireVictory = pygame.image.load("images/firevictory.png")
        self.fireVictory = pygame.transform.scale(self.fireVictory, 
            (int(data.PLAY_GRID_SIZE * 1.25 * 16 / 29), int(data.PLAY_GRID_SIZE * 1.25)))


    def setImage(self, data):
        # decides which sprite to use at any given frame, essentially handles
        # animating Mario's walk cycle

        if(self.invul and self.invulCount % 2 == 1 and not self.completed):
            # self.image = self.smallLeftSprites[0]
            width, height = self.image.get_width(), self.image.get_height()
            self.image = pygame.Surface((width, height))
            self.image.fill(data.WHITE)
            self.image.set_colorkey(data.WHITE)

        elif(self.state == "small"):
            if(self.faceDir == "left"):
                if(self.vy < 0):
                    self.image = self.smallLeftJumpSprite
                elif(self.vy > 0):
                    self.image = self.smallLeftFallingSprite
                elif(self.vx == 0):
                    self.image = self.smallLeftSprites[0]
                elif(self.vx <= 0):
                    self.image = self.smallLeftSprites[self.tick % 4]
            elif(self.faceDir == "right"):
                if(self.vy < 0):
                    self.image = self.smallRightJumpSprite
                elif(self.vy > 0):
                    self.image = self.smallRightFallingSprite
                elif(self.vx == 0):
                    self.image = self.smallRightSprites[0]
                elif(self.vx >= 0):
                    self.image = self.smallRightSprites[self.tick % 4]

        elif(self.state == "super"):
            if(self.faceDir == "left"):
                if(self.vy < 0):
                    self.image = self.superLeftJumpSprite
                elif(self.vy > 0):
                    self.image = self.superLeftFallingSprite
                elif(self.vx == 0):
                    self.image = self.superLeftSprites[0]
                elif(self.vx <= 0):
                    self.image = self.superLeftSprites[self.tick % 4]
            elif(self.faceDir == "right"):
                if(self.vy < 0):
                    self.image = self.superRightJumpSprite
                elif(self.vy > 0):
                    self.image = self.superRightFallingSprite
                elif(self.vx == 0):
                    self.image = self.superRightSprites[0]
                elif(self.vx >= 0):
                    self.image = self.superRightSprites[self.tick % 4]

        elif(self.state == "fire"):
            if(self.faceDir == "left"):
                if(self.vy < 0):
                    self.image = self.fireLeftJumpSprite
                elif(self.vy > 0):
                    self.image = self.fireLeftFallingSprite
                elif(self.vx == 0):
                    self.image = self.fireLeftSprites[0]
                elif(self.vx <= 0):
                    self.image = self.fireLeftSprites[self.tick % 3]
            elif(self.faceDir == "right"):
                if(self.vy < 0):
                    self.image = self.fireRightJumpSprite
                elif(self.vy > 0):
                    self.image = self.fireRightFallingSprite
                elif(self.vx == 0):
                    self.image = self.fireRightSprites[0]
                elif(self.vx >= 0):
                    self.image = self.fireRightSprites[self.tick % 3]
        self.image = self.image.convert_alpha()

    def isOnBlock(self, data):
        # checks if Mario is currently on top of a block object

        self.rect.y += 2
        blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        if(blockCollisions != []):
            for entity in blockCollisions:
                if(self.rect.bottom > entity.rect.top):
                    self.rect.y -= 2
                    return True
        self.rect.y -= 2
        return False

        # self.rect.y += self.COLLISION_MARGIN
        # blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
        # self.rect.y -= self.COLLISION_MARGIN
        # if(blockCollisions != []):
        #     return True
        # return False


    def updateValues(self):
        self.width, self.height = self.image.get_size()
        # self.rect = self.image.get_rect()
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def update(self, data):
        if(self.living == False and self.deathTicks == 0):
            self.image = self.deadSprite
            self.rect.y -= 10
            self.y = self.rect.y
            try:
                pygame.mixer.music.load(data.deathMusic)
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play()
            except:
                pass
        if(self.living == False and self.deathTicks < 10):
            self.image = self.deadSprite
            self.deathTicks += 1
        elif(self.living == False and self.deathTicks >= 10 and self.deathTicks < 75):
            self.image = self.deadSprite
            self.rect.y += 5
            self.y = self.rect.y
            self.deathTicks += 1
        elif(self.living == False and self.deathTicks >= 75):
            data.mode = "gameOver"
        else:
            self.setImage(data)
            print(self.vx)
            if(self.completed and self.winTicks < 60):
                print("win")
                self.vx = 4
                self.invul = True
                self.winTicks += 1
                self.setImage(data)
                self.tick += 1
            elif(self.completed and self.winTicks >= 60 and self.winTicks < 160):
                self.vx = 0
                if(self.state == "small"):
                    self.image = self.smallVictory
                elif(self.state == "super"):
                    self.image = self.superVictory
                elif(self.state == "fire"):
                    self.image = self.fireVictory
                self.winTicks += 1
            elif(self.completed and self.winTicks >= 160):
                data.mode = "winScreen"
            

            if(self.invul and self.invulCount < 60):
                self.invulCount += 1
            elif(self.invul and self.invulCount >= 60):
                self.invul = False
                self.invulCount = 0

            if(self.decelerating):
                self.decelerate()

            if(self.absX >= 0):
                self.x += self.vx
                self.y += self.vy

                self.absX += self.vx
                self.absY += self.vy
            else:
                self.x = 1
                self.absX = 1
                self.vx = 0

            if(self.absX <= 0):
                self.x, self.absX = 0, 0
                self.vx = 0

            if(self.absY > len(data.level.getMap()) * data.PLAY_GRID_SIZE and not self.completed):
                self.living = False

            if(self.x < data.X_SCROLL_MARGIN or self.x > data.width - data.X_SCROLL_MARGIN):
                self.horizScroll(data)

            if(self.y < data.Y_SCROLL_MARGIN or self.y > data.height - data.Y_SCROLL_MARGIN):
                self.vertScroll(data)

            self.rect.x, self.rect.y = self.x, self.y + 1
            self.top, self.bottom = self.rect.midtop, self.rect.midbottom
            self.left, self.right = self.rect.midleft, self.rect.midright

            # self.x += self.vx
            # self.absX += self.vx

            self.blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
            self.enemyCollisions = pygame.sprite.spritecollide(self, data.enemyGroup, False)
            self.itemCollisions = pygame.sprite.spritecollide(self, data.itemGroup, False)

            # if(self.x < data.X_SCROLL_MARGIN or self.x > data.width - data.X_SCROLL_MARGIN):
            #     self.horizScroll(data)

            # self.rect.x = self.x

            # self.testHorizCollisions(data)

            # self.y += self.vy
            # self.absY += self.vy

            # self.blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)
            # self.enemyCollisions = pygame.sprite.spritecollide(self, data.enemyGroup, False)
            # self.itemCollisions = pygame.sprite.spritecollide(self, data.itemGroup, False)

            # if(self.y < data.Y_SCROLL_MARGIN or self.y > data.height - data.Y_SCROLL_MARGIN):
            #     self.vertScroll(data)

            # self.rect.y = self.y

            # self.testVertCollisions(data)


            self.testBlockCollisions(data)
            self.testEnemyCollisions(data)
            self.testItemCollisions(data)


            # self.rect.x, self.rect.y = self.x, self.y

            if(self.absX < 0):
                self.absX = 0
                self.rect.x = 0

            self.x, self.y = self.rect.x, self.rect.y



    def horizScroll(self, data):
        if(self.x < data.X_SCROLL_MARGIN and self.absX > data.width - data.X_SCROLL_MARGIN):
            data.xOffsetPlayPix += self.vx
            self.x = data.X_SCROLL_MARGIN
        elif(self.x > data.width - data.X_SCROLL_MARGIN):
            data.xOffsetPlayPix += self.vx
            data.xOffsetPlay = data.xOffsetPlayPix // data.PLAY_GRID_SIZE
            self.x = data.width - data.X_SCROLL_MARGIN

    def vertScroll(self, data):
        if(self.y < data.Y_SCROLL_MARGIN and self.absY > data.height - data.Y_SCROLL_MARGIN):
            data.yOffsetPlayPix += self.vx
            self.y = data.Y_SCROLL_MARGIN
        elif(self.x > data.height - data.Y_SCROLL_MARGIN):
            data.yOffsetPlayPix -= self.vx
            self.y = data.height - data.Y_SCROLL_MARGIN

    def testHorizCollisions(self, data):
        self.testBlockCollisions(data, "horiz")

    def testVertCollisions(self, data):
        self.testBlockCollisions(data, "vert")

    def testBlockCollisions(self, data, axis = "vert"):
        if(self.blockCollisions != []):
            for entity in self.blockCollisions:
                # if(self.vy > 0):
                if(entity.rect.collidepoint((self.bottom[0] + self.COLLISION_MARGIN, self.bottom[1]))):
                    # player above collided entity
                    print('above')
                    if(isinstance(entity, blocks.EndPole)):
                        self.blockCollideTop(data, entity)
                    elif(not isinstance(entity, blocks.Brick) or 
                        (isinstance(entity, blocks.Brick) and not entity.spinning)):
                        self.vy = 0
                        self.rect.bottom = entity.rect.top - self.COLLISION_MARGIN
                        self.blockCollideTop(data, entity)
                # elif(self.vy < 0):
                elif(entity.rect.collidepoint((self.top[0] - self.COLLISION_MARGIN, self.top[1]))):
                    #player below collided entity
                    print('below')
                    if(isinstance(entity, blocks.EndPole)):
                        self.blockCollideBottom(data, entity)
                    elif(not isinstance(entity, blocks.Brick) or 
                        (isinstance(entity, blocks.Brick) and not entity.spinning)):
                        if(not isinstance(entity, blocks.Platform)):
                            self.vy = 0
                            self.rect.top = entity.rect.bottom + self.COLLISION_MARGIN
                            self.blockCollideBottom(data, entity)
        if(self.blockCollisions != []):
            for entity in self.blockCollisions:
                # if(self.vx > 0):
                if((entity.rect.collidepoint((self.right[0] + self.COLLISION_MARGIN, self.right[1])))):
                    # player left of collided entity
                    print('left')
                    if(isinstance(entity, blocks.EndPole)):
                        self.blockCollideLeft(data, entity)
                    elif(not isinstance(entity, blocks.Brick) or 
                        (isinstance(entity, blocks.Brick) and not entity.spinning)):
                        if(not isinstance(entity, blocks.Platform)):
                            self.vx = 0
                            self.rect.right = entity.rect.left - self.COLLISION_MARGIN
                            self.blockCollideLeft(data, entity)
                # elif(self.vx < 0):
                elif(entity.rect.collidepoint((self.left[0] - self.COLLISION_MARGIN, self.left[1]))):
                    #player right of collided entity
                    print('right')
                    if(isinstance(entity, blocks.EndPole)):
                        self.blockCollideRight(data, entity)
                    elif(not isinstance(entity, blocks.Brick) or 
                        (isinstance(entity, blocks.Brick) and not entity.spinning)):
                        if(not isinstance(entity, blocks.Platform)):
                            self.vx = 0
                            self.rect.left = entity.rect.right + self.COLLISION_MARGIN
                            self.blockCollideRight(data, entity)

        

    def blockCollideLeft(self, data, entity):
        if(isinstance(entity, blocks.Spike)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small"):
                self.living = False
        if(isinstance(entity, blocks.EndPole)):
            self.completed = True
            self.winTicks = 0
            self.vy = 0
            try:
                pygame.mixer.music.load(data.clearMusic)
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play()
            except:
                pass

    def blockCollideRight(self, data, entity):
        if(isinstance(entity, blocks.Spike)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small"):
                self.living = False
        if(isinstance(entity, blocks.EndPole)):
            self.completed = True
            self.winTicks = 0
            self.vy = 0
            try:
                pygame.mixer.music.load(data.clearMusic)
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play()
            except:
                pass

    def blockCollideTop(self, data, entity):
        if(isinstance(entity, blocks.FallingPlatform)):
            entity.activate(data)
            self.vy = entity.vy
        if(isinstance(entity, blocks.Spike)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small"):
                self.living = False
        if(isinstance(entity, blocks.EndPole)):
            self.completed = True
            self.winTicks = 0
            self.vy = 0
            try:
                pygame.mixer.music.load(data.clearMusic)
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play()
            except:
                pass

    def blockCollideBottom(self, data, entity):
        if(isinstance(entity, blocks.Question)):
            if(entity.getItem() != None):
                entity.spawnItem(data)
        if(isinstance(entity, blocks.Brick)):
            if(not entity.spinning):
                entity.spin()
        if(isinstance(entity, blocks.Spike) and not self.invul):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small"):
                self.living = False
        if(isinstance(entity, blocks.EndPole)):
            self.completed = True
            self.winTicks = 0
            self.vy = 0
            try:
                pygame.mixer.music.load(data.clearMusic)
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play()
            except:
                pass


    def testEnemyCollisions(self, data):
        if(self.enemyCollisions != []):
            for entity in self.enemyCollisions:
                # if(self.right - self.COLLISION_MARGIN > entity.rect.left):
                if((entity.rect.collidepoint((self.right[0] + self.COLLISION_MARGIN, self.right[1])))):
                    # player left of collided entity
                    self.vx = 0
                    self.rect.right = entity.rect.left - self.COLLISION_MARGIN
                    self.enemyCollideLeft(data, entity)
                elif(entity.rect.collidepoint((self.left[0] - self.COLLISION_MARGIN, self.left[1]))):
                    #player right of collided entity
                    self.vx = 0
                    self.rect.left = entity.rect.right + self.COLLISION_MARGIN
                    self.enemyCollideRight(data, entity)

        if(self.enemyCollisions != [] and self.vy != 0):
            for entity in self.enemyCollisions:
                # if(self.bottom - self.COLLISION_MARGIN > entity.rect.top):
                if(entity.rect.collidepoint((self.bottom[0] + self.COLLISION_MARGIN, self.bottom[1]))):
                    # player above collided entity
                    self.vy = 0
                    self.rect.bottom = entity.rect.top - self.COLLISION_MARGIN
                    self.enemyCollideTop(data, entity)
                elif(entity.rect.collidepoint((self.top[0] - self.COLLISION_MARGIN, self.top[1]))):
                    #player below collided entity
                    self.vy = 0
                    self.rect.top = entity.rect.bottom - self.COLLISION_MARGIN
                    self.enemyCollideBottom(data, entity)

    def enemyCollideLeft(self, data, entity):
        if(not isinstance(entity, enemies.Blaster) and not isinstance(entity, enemies.BulletShooter)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small" and not self.invul):
                self.living = False

    def enemyCollideRight(self, data, entity):
        if(not isinstance(entity, enemies.Blaster) and not isinstance(entity, enemies.BulletShooter)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small" and not self.invul):
                self.living = False

    def enemyCollideTop(self, data, entity):
        if(not isinstance(entity, enemies.Blaster) and 
            not isinstance(entity, enemies.BulletShooter)):
            if(entity.jumpable == True):
                data.stompSFX.play()
                self.vx = -3
                entity.deathSequence(data)
            else:
                if(self.state == "fire" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "super"
                    self.invul = True
                elif(self.state == "super" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "small"
                    self.invul = True
                elif(self.state == "small" and not self.invul):
                    self.living = False

    def enemyCollideBottom(self, data, entity):
        if(not isinstance(entity, enemies.Blaster) and 
            not isinstance(entity, enemies.BulletShooter)):
            if(self.state == "fire" and not self.invul):
                data.powerdownSFX.play()
                self.state = "super"
                self.invul = True
            elif(self.state == "super" and not self.invul):
                data.powerdownSFX.play()
                self.state = "small"
                self.invul = True
            elif(self.state == "small" and not self.invul):
                self.living = False


    def testItemCollisions(self, data):
        if(self.itemCollisions != []):
            for entity in self.itemCollisions:
                if(entity != self.held):
                    if((entity.rect.collidepoint((self.right[0] + self.COLLISION_MARGIN, self.right[1])))):
                        # player left of collided entity
                        print('left')
                        self.vx = 0
                        self.rect.right = entity.rect.left - self.COLLISION_MARGIN
                        self.itemCollideLeft(data, entity)
                    elif(entity.rect.collidepoint((self.left[0] - self.COLLISION_MARGIN, self.left[1]))):
                        #player right of collided entity
                        print('right')
                        self.vy = 0
                        self.rect.left = entity.rect.right + self.COLLISION_MARGIN
                        self.itemCollideRight(data, entity)

        if(self.itemCollisions != []):
            for entity in self.itemCollisions:
                if(entity != self.held):
                    if(entity.rect.collidepoint((self.bottom[0] + self.COLLISION_MARGIN, self.bottom[1]))):
                        # player above collided entity
                        print('above')
                        self.vy = 0
                        self.rect.bottom = entity.rect.top - self.COLLISION_MARGIN
                        self.itemCollideTop(data, entity)
                    elif(entity.rect.collidepoint((self.top[0] - self.COLLISION_MARGIN, self.top[1]))):
                        #player below collided entity
                        print('below')
                        self.vy = 0
                        self.rect.top = entity.rect.bottom + self.COLLISION_MARGIN
                        self.itemCollideBottom(data, entity)

    def itemCollideLeft(self, data, entity):
        if(isinstance(entity, items.Shell)):
            if(entity.active):
                if(self.state == "fire" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "super"
                    self.invul = True
                elif(self.state == "super" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "small"
                    self.invul = True
                elif(self.state == "small" and not self.invul):
                    self.living = False
            else:
                if(self.grabbing):
                    entity.grabbed(data, "left")
                    self.held = entity
                else:
                    entity.setActive("right")
        if(isinstance(entity, items.Mushroom)):
            data.powerupSFX.play()
            if(self.state != "fire"):
                self.state = "super"
            self.y -= 5
            entity.kill()
        if(isinstance(entity, items.FireFlower)):
            data.powerupSFX.play()
            self.state = "fire"
            self.y -= 5
            entity.kill()

    def itemCollideRight(self, data, entity):
        if(isinstance(entity, items.Shell)):
            if(entity.active):
                if(entity.active):
                    if(self.state == "fire" and not self.invul):
                        data.powerdownSFX.play()
                        self.state = "super"
                        self.invul = True
                    elif(self.state == "super" and not self.invul):
                        data.powerdownSFX.play()
                        self.state = "small"
                        self.invul = True
                    elif(self.state == "small" and not self.invul):
                        self.living = False
            else:
                if(self.grabbing):
                    entity.grabbed(data, "right")
                    self.held = entity
                else:
                    entity.setActive("left")
        if(isinstance(entity, items.Mushroom)):
            data.powerupSFX.play()
            print("kill")
            if(self.state != "fire"):
                self.state = "super"
            self.y -= 5
            entity.kill()
        if(isinstance(entity, items.FireFlower)):
            data.powerupSFX.play()
            self.state = "fire"
            self.y -= 5
            entity.kill()

    def itemCollideTop(self, data, entity):
        if(isinstance(entity, items.Shell)):
            if(entity.active):
                entity.stopActive()
                self.vy -= 3
            elif(not entity.active):
                direction = "right" if(self.vx >= 0) else "left"
                entity.setActive(direction)
        if(isinstance(entity, items.Mushroom)):
            data.powerupSFX.play()
            print("kill")
            if(self.state != "fire"):
                self.state = "super"
            self.y -= 5
            entity.kill()
        if(isinstance(entity, items.FireFlower)):
            data.powerupSFX.play()
            self.state = "fire"
            self.y -= 5
            entity.kill()

    def itemCollideBottom(self, data, entity):
        if(isinstance(entity, items.Shell)):
            if(entity.active):
                if(self.state == "fire" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "super"
                    self.invul = True
                elif(self.state == "super" and not self.invul):
                    data.powerdownSFX.play()
                    self.state = "small"
                    self.invul = True
                elif(self.state == "small" and not self.invul):
                    self.living = False
        if(isinstance(entity, items.Mushroom)):
            data.powerupSFX.play()
            print("kill")
            if(self.state != "fire"):
                self.state = "super"
            self.y -= 5
            entity.kill()
        if(isinstance(entity, items.FireFlower)):
            data.powerupSFX.play()
            self.state = "fire"
            self.y -= 5
            entity.kill()

    def updateEvent(self, data, key, eventType):
        if(not self.completed):
            if(eventType == "keyPress"):
                self.updateKeyPress(data, key)
            elif(eventType == "keyHeld"):
                self.updateKeyHeld(data, key)
            elif(eventType == "keyReleased"):
                self.updateKeyReleased(data, key)
        if(eventType == "timerFired"):
            self.timer(data)
        self.updateValues()
        self.update(data)
        # print(self.rect.x, self.rect.y)
        # print(self.rect)

    def updateKeyPress(self, data, key):
        if(key == K_ESCAPE):
            try:
                pygame.mixer.music.load(data.menuMusic)
                pygame.mixer.music.set_volume(.125)
                pygame.mixer.music.play()
            except:
                pass
            data.mode = "designer"
        elif(not self.completed):
            if(key == K_LEFT):
                self.leftPressed = True
                self.faceDir = "left"
            elif(key == K_RIGHT):
                self.rightPressed = True
                self.faceDir = "right"
            if(key == K_SPACE):
                self.playerJump(data)
            elif(key == K_x):
                self.playerAction(data)

        
    def updateKeyHeld(self, data, key):
        if(key == K_LEFT):
            self.playerMoveLeft(data)
        elif(key == K_RIGHT):
            self.playerMoveRight(data)
        elif(key == K_z):
            self.playerGrabItem(data)

    def playerMoveLeft(self, data):
        self.tick += 1
        if(self.leftPressed):
            self.vx = -3
            self.leftPressed = False
        elif(not self.leftPressed and self.vx > -4.5):
            self.vx -= .1

    def playerMoveRight(self, data):
        self.tick += 1
        if(self.rightPressed):
            self.vx = 3
            self.rightPressed = False
        elif(not self.rightPressed and self.vx < 4.5):
            self.vx += .1

    def playerGrabItem(self, data):
        self.grabbing = True

    def updateKeyReleased(self, data, event):
        if(event.key == K_LEFT or event.key == K_RIGHT):
            self.decelerating = True
            self.tick = 0
        elif(event.key == K_z):
            print("sjdhfjsdhfjkshdfkjsd")
            self.grabbing = False
            self.playerReleaseItem(data)

    def playerReleaseItem(self, data):
        if(self.held != None):
            if(self.faceDir == "left"):
                self.held.setActive("left")
            elif(self.faceDir == "right"):
                self.held.setActive("right")
    
    def timer(self, data):
        if(not self.isOnBlock(data)):
            if(self.vy == 0):
                self.vy = 1.5
            self.vy += data.gravity

    def playerJump(self, data):
        if(self.isOnBlock(data)):
            data.jumpSFX.play()
            self.vy = -7

    def decelerate(self):
        if(self.vx > .5):
            self.vx -= .3
        elif(self.vx < -.5):
            self.vx += .3
        else:#(self.vx == 0):
            self.vx = 0
            self.decelerating = False

    def playerAction(self, data):
        if(self.state == "fire" and data.fireballs <= 2):
            data.fireballs += 1
            data.fireSFX.play()
            x, y = self.rect.midright
            data.fireGroup.add(Fireball(x, y, data, self.faceDir))


class Fireball(pygame.sprite.Sprite):

    def __init__(self, x, y, data, faceDir):
        super().__init__()
        self.x, self.y = x, y

        TILE_SPRITES = utils.SpriteSheet("images/enemies.gif")
        self.image = TILE_SPRITES.extractSprite(379, 271, 6, 7)
        self.image = pygame.transform.scale(self.image, (data.PLAY_GRID_SIZE // 3, data.PLAY_GRID_SIZE // 3))

        self.peakY = self.y - 25
        self.ticks = 0

        self.faceDir = faceDir

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        if(self.faceDir == "right"):
            self.vx, self.vy = 5, 5
        elif(self.faceDir):
            self.vx, self.vy = -5, 5

    def update(self, data):
        if(self.ticks >= 100):
            self.kill()
            data.fireballs -= 1

        self.blockCollisions = pygame.sprite.spritecollide(self, data.platformGroup, False)

        print(self.blockCollisions)
        if(self.y <= self.peakY):
            self.vx = 5 if self.faceDir == "right" else -5
            self.vy = 5

        if(self.blockCollisions != []):
            print('collided')
            self.vy = -5

        self.enemyCollisions = pygame.sprite.spritecollide(self, data.enemyGroup, False)

        if(self.enemyCollisions != []):
            if(not isinstance(self.enemyCollisions[0], enemies.Blaster) and
                not isinstance(self.enemyCollisions[0], enemies.BulletShooter)):
                self.kill()
                self.enemyCollisions[0].kill()
                data.fireballs -= 1

        self.x += self.vx
        self.y += self.vy

        if(data.xOffsetPlayPix > 0):
            self.offsetX = self.x - data.xOffsetPlayPix
        else:
            self.offsetX = self.x
        if(data.yOffsetPlayPix > 0):
            self.offsetY = self.y - data.yOffsetPlayPix
        else:
            self.offsetY = self.y

        self.ticks += 1
        self.rect.x, self.rect.y = self.offsetX, self.offsetY