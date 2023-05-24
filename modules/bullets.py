import pygame
import math
from modules.constants import BULLET_STAT_TABLE

class Bullet():
    def __init__(self, x, y, angle, shotBy, type="standard"):
        """
        type options:
        
        """
        self.x = x
        self.y = y
        self.angle = angle

        self.velocity = BULLET_STAT_TABLE[type]["velocity"]
        self.radius = BULLET_STAT_TABLE[type]["reload"]
        self.shotBy = shotBy
        self.type = type
        self.damage = BULLET_STAT_TABLE[type]["damage"]
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
    
    def update(self):
        self.x -= math.cos(self.angle) * self.velocity
        self.y -= math.sin(self.angle) * self.velocity