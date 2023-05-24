import pygame
from modules.constants import *
import math
from modules.functions import *
from random import randint

class Particle():
    def __init__(self, x, y, color=(78, 164, 95)):
        self.size = randint(6, 8)
        self.x = x
        self.y = y-self.size
        self.groundY = y

        self.yVel = -randint(0, 8)
        self.xvel = randint(-3, 3)
        self.color = color
        self.life = 100
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def update(self, dt):
        self.y += self.yVel * dt
        self.yVel += GRAVITY * dt

        if self.y >= self.groundY-self.size:
            self.yVel = 0
            self.y = self.groundY - self.size
        
        self.life -= 1

class Player():
    def __init__(self, startPos, color, inputMap, bulletClass, name, image, camera):
        self.startX = startPos[0]
        self.startY = startPos[1]
        self.name = name.capitalize()
        self.image = image
        self.camera = camera

        # position and velocity
        self.x = self.startX
        self.y = self.startY

        self.yVel = 0
        self.xVel = 0
        self.jumpVel = -20
        self.acceleration = 1.5
        self.maxSpeed = 5
        self.friction = 0.2
        
        # size
        self.w = PLAYER_SIZE
        self.h = PLAYER_SIZE

        # color
        self.color = color

        self.onBlock = False
        self.doubleJump = True
        self.inputMap = inputMap
        self.bulletClass = bulletClass
        self.reload = 0
        self.reloadTime = 10
        self.dir = 0
        self.health = 100
        self.angle = 0
        self.angleTo = 0
        self.particles = []
        self.frame = 0

    def respawn(self):
        self.x = self.startX
        self.y = self.startY
        self.yVel = 0
        self.xVel = 0

    def draw(self, screen, dt):
        for p in reversed(self.particles):
            p.draw(screen)
            p.update(dt)
            if p.life < 0:
                self.particles.remove(p)

        playerImg = self.image.copy()
        if int(self.angle)%360 != 0: playerImg = pygame.transform.rotate(playerImg, int(self.angle))
        playerImg = pygame.transform.flip(playerImg, False if self.dir < 0 else True, False)
        
        
        screen.blit(playerImg, ((self.x - playerImg.get_width()/2) + self.w/2, (self.y - playerImg.get_height()/2) + self.h/2))
        #health bar
        pygame.draw.rect(screen, (0, 100, 50), (self.x + self.w/2 - self.health/4, self.y - 20, self.health/2, 10))

    def update(self, blocks, inputs, doubleInput, dt):
        self.angle = lerp(self.angle, self.angleTo, 0.15)
        self.frame += dt

        if self.y > 10000:
            self.respawn()
            self.health -= 50

        # move then check for collisions on the y axis
        self.y += self.yVel * dt
        self.yVel += GRAVITY * dt

        for block in blocks:
            if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(block.rect):
                
                if self.yVel > 25:
                    self.camera.shake += self.yVel/2

                self.yVel = 0

                if self.y < block.rect.y:
                    self.y = block.rect.y - self.h
                    self.onBlock = True
                    
                else:
                    self.y = block.rect.y + block.rect.h

        # move then check for collisions on the x axis
        if self.inputMap[1] in inputs:
            if int(self.frame)%8 == 0 and self.onBlock: self.particles.append(Particle(self.x+randint(0, self.w), self.y+self.h))
            
            self.xVel -= self.acceleration * dt
            if self.inputMap[1] in doubleInput: 
                self.x -= 200
                self.camera.shake += 5
                self.angleTo -= 360
            self.dir = 0
        if self.inputMap[3] in inputs:
            if int(self.frame)%8 == 0 and self.onBlock: self.particles.append(Particle(self.x+randint(0, self.w), self.y+self.h))

            self.xVel += self.acceleration * dt
            if self.inputMap[3] in doubleInput: 
                self.x += 200
                self.camera.shake += 5
                self.angleTo -= 360
            self.dir = -math.pi
        
        
        self.xVel = clamp(self.xVel, -self.maxSpeed, self.maxSpeed)
        self.x += self.xVel * dt
        self.xVel *= 1 - self.friction

        for block in blocks:
            if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(block.rect):
                self.xVel = 0

                if self.x < block.rect.x:
                    self.x = block.rect.x - self.w
                else:
                    self.x = block.rect.x + block.rect.w
        
        # jump if on a block and jump key pressed
        if self.onBlock and self.inputMap[0] in inputs:
            self.yVel = self.jumpVel
            self.onBlock = False
            self.doubleJump = True
            del inputs[self.inputMap[0]]
        elif self.doubleJump and self.inputMap[0] in inputs:
            self.yVel = self.jumpVel
            self.doubleJump = False
        

    def handleBullets(self, inputs, bulletList, dt):
        for b in bulletList:
            if b.shotBy != self and pygame.Rect(self.x, self.y, self.w, self.h).collidepoint(b.x, b.y):
                bulletList.remove(b)
                self.health -= 5
                self.camera.shake += 5
        
        if self.inputMap[2] in inputs and self.reload < 0:
            bulletList.append(self.bulletClass(self.x+self.w/2, self.y+self.h/2, self.dir, self))
            self.reload = self.reloadTime
            

        self.reload -= 1 * dt
        