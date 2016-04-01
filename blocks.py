import pygame

class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

class Platform(Block):

    def __init__(self, x, y):
        super().__init__()
        