import pygame

class Crate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
    
    


class Block():
    def __init__(self, position):
        self.rect = pygame.Rect(position)