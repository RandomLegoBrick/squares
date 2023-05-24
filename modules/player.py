import pygame
from modules.constants import *
import math
from modules.functions import *

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
        
    def respawn(self):
        self.x = self.startX
        self.y = self.startY
        self.yVel = 0
        self.xVel = 0

    def draw(self, screen):
        playerImg = pygame.transform.flip(self.image, False if self.dir < 0 else True, False)

        screen.blit(playerImg, (self.x, self.y))
        #health bar
        pygame.draw.rect(screen, (0, 100, 50), (self.x + self.w/2 - self.health/4, self.y - 20, self.health/2, 10))

    def update(self, blocks, inputs, doubleInput):
        if self.y > 10000:
            self.respawn()
            self.health -= 50

        # move then check for collisions on the y axis
        self.y += self.yVel
        self.yVel += GRAVITY

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
            self.xVel -= self.acceleration
            if self.inputMap[1] in doubleInput: self.x -= 100
            self.dir = 0
        if self.inputMap[3] in inputs:
            self.xVel += self.acceleration
            if self.inputMap[3] in doubleInput: self.x += 100
            self.dir = -math.pi
        
        
        self.xVel = clamp(self.xVel, -self.maxSpeed, self.maxSpeed)
        self.x += self.xVel
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
        

    def handleBullets(self, inputs, bulletList):
        for b in bulletList:
            if b.shotBy != self and pygame.Rect(self.x, self.y, self.w, self.h).collidepoint(b.x, b.y):
                bulletList.remove(b)
                self.health -= 5
                self.camera.shake += 5
        
        if self.inputMap[2] in inputs and self.reload < 0:
            bulletList.append(self.bulletClass(self.x+self.w/2, self.y+self.h/2, self.dir, self))
            self.reload = self.reloadTime
            

        self.reload -= 1
        