import pygame
from pygame.locals import *
from modules.constants import *
from modules import player, blocks, bullets


pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

clock = pygame.time.Clock()
running = True
inputs = {}

mapBlocks = [blocks.Block(b, (200, 200, 200)) for b in [(width/2 - 250, height/2 - 10, 500, 20)]]
players = [player.Player((width/2 - 150, 100), (255, 50, 50), [K_w, K_a, K_s, K_d], bullets.Bullet, "Matthew"), player.Player((width/2 + 150, 100), (50, 255, 50), [K_UP, K_LEFT, K_DOWN, K_RIGHT], bullets.Bullet, "Justin")]
bulletList = []

def textCentered(msg, x, y, size, color):
    font = pygame.font.SysFont("Segoe UI Black", size)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == VIDEORESIZE:
            width, height = e.w, e.h
        elif e.type == KEYDOWN:
            inputs[e.key] = True
        elif e.type == KEYUP and e.key in inputs:
            del inputs[e.key]
    
    screen.fill(BACKGROUND)
    
    for block in mapBlocks:
        block.draw(screen)

    for bullet in bulletList:
        bullet.draw(screen)
        bullet.update()

    for n, p in enumerate(players):
        p.draw(screen)
        p.update(mapBlocks, inputs)
        p.handleBullets(inputs, bulletList)

        if(p.health <= 0):
            players.pop(n)
    
    if len(players) == 1:
        textCentered(f"{players[0].name} wins!", width/2, height/2, 100, (0, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()