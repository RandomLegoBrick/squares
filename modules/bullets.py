import pygame
import math
from modules.constants import BULLET_STAT_TABLE

weapon_textures = {}

def init(textures):
    global weapon_textures
    weapon_textures = textures

class Bullet():
    def __init__(self, x, y, angle, shotBy, type="standard"):
        """
        type options:
        
        """
        self.x = x
        self.y = y
        self.angle = angle

        self.velocity = BULLET_STAT_TABLE[type]["velocity"]
        self.shotBy = shotBy
        self.type = type
        self.damage = BULLET_STAT_TABLE[type]["damage"]
        self.img = weapon_textures["bullet_"+self.type]
        self.radius = self.img.get_width()/2
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, (self.x-self.radius, self.y-self.radius))
    
    def update(self, dt):
        self.x -= math.cos(self.angle) * self.velocity * dt
        self.y -= math.sin(self.angle) * self.velocity * dt