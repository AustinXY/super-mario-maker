import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, faceDir):
        super().__init__()
        self.x = x
        self.y = y
        self.faceDir = faceDir

class Goomba(Enemy):

    def __init__(self, x, y, winged, faceDir):
        super().__init__(x, y, faceDir)
        self.winged = winged

class Koopa(Enemy):
    
    def __init__(self, x, y, color, winged, faceDir):
        super().__init__(x, y, faceDir)
        self.winged = winged

class DryBones(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)
        self.crumbled = False

class HammerBros(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class BuzzyBeetle(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class Spiny(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class Lakitu(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class CheepCheep(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class Boo(Enemy):

    def __init__(self, x, y, faceDir):
        super().__init__(x, y, faceDir)

class Bobomb(Enemy):

    def __init__(self, x, y, active, faceDir):
        super().__init__(x, y, faceDir)
        self.active = active
        self.faceDir = faceDir