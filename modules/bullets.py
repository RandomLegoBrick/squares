import pygame
import math
from modules.constants import *

weapon_textures = {}
explosion_frames = []

def init(textures):
    global weapon_textures
    weapon_textures = textures

    sprite = pygame.image.load(explosion_textures[0])
    for i in range(8):
        surf = pygame.surface.Surface((16, 16)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        surf.blit(sprite, (0, 0), (i*16, 0, 16, 16))
        explosion_frames.append(pygame.transform.scale(surf, (16 * 12, 16 * 12)))


class Bullet():
    def __init__(self, x, y, dir, shotBy, type="standard"):
        """
        type options:
        
        """
        self.x = x
        self.y = y
        self.dir = dir

        self.velocity = BULLET_STAT_TABLE["bullet_"+type]["velocity"]
        self.shotBy = shotBy
        self.type = type
        self.damage = BULLET_STAT_TABLE["bullet_"+type]["damage"]
        self.img = weapon_textures["bullet_"+self.type]
        self.radius = self.img.get_width()/2
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, (self.x-self.radius, self.y-self.radius))
    
    def update(self, dt):
        self.x -= self.dir * self.velocity * dt

class Grenade():
    def __init__(self, x, y, dir, shotBy, type="standard"):
        self.x = x
        self.y = y
        self.yVel = -BULLET_STAT_TABLE["grenade_"+type]["velocity"]
        self.xVel = dir * BULLET_STAT_TABLE["grenade_"+type]["velocity"]
        self.shotBy = shotBy
        self.type = type
        self.damage = BULLET_STAT_TABLE["grenade_"+type]["damage"]
        self.img = weapon_textures["grenade_"+self.type]
        self.size = self.img.get_width()
        self.friction = 0.2
        self.timer = 100
        self.blastRadius = 100
        self.minDamage = 20
        self.maxDamage = 60
    
    def draw(self, screen: pygame.Surface):
        if self.timer > 4*4: ## hide the grenade 4 frames into the explosion
            screen.blit(self.img, (self.x, self.y))
        
        if self.timer < 8*4:
            screen.blit(explosion_frames[7-int(self.timer/4)], (self.x-explosion_frames[0].get_width()/2 + self.size/2, 
                                                                self.y-explosion_frames[0].get_height()/2 + self.size/2))
    
    def update(self, blocks, camera, players, dt):
        self.timer -= 1 * dt

        if int(self.timer) == 8*4:
            camera.shake += 10


        py = self.y
        self.y += self.yVel * dt
        self.yVel += GRAVITY * dt

        for b in blocks:
            if pygame.rect.Rect(self.x, self.y, self.size, self.size).colliderect(b.rect):
                self.yVel = 0
                self.xVel *= (1 - self.friction)

                if py < b.rect.y:
                    self.y = b.rect.y - self.size
                else:
                    self.y = b.rect.y + b.rect.h

        px = self.x
        self.x -= self.xVel * dt

        for b in blocks:
            if pygame.rect.Rect(self.x, self.y, self.size, self.size).colliderect(b.rect):
                self.xVel = 0

                if px < b.rect.x:
                    self.x = b.rect.x - self.size
                else:
                    self.x = b.rect.x + b.rect.w
