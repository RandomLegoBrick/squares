import pygame
import math

class Bullet():
    def __init__(self, x, y, angle, shotBy):
        self.x = x
        self.y = y
        self.angle = angle

        self.velocity = 50
        self.radius = 5
        self.shotBy = shotBy
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
    
    def update(self):
        self.x -= math.cos(self.angle) * self.velocity
        self.y -= math.sin(self.angle) * self.velocity