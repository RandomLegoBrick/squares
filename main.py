import pygame
from pygame.locals import *
from modules.constants import *
from modules import player, blocks, bullets

### Enviornment Variables ###
pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

### Input Variables ###
inputs = {}
inputTime = {} # Stores the time of the last input for each key
doubleInput = {} # Keep track of double strokes

### Load Textures ###
def load(path, pixel_size=PIXEL_SIZE):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * pixel_size, img.get_height() * pixel_size))
    return img

for current_map in map_textures:
    for texture in map_textures[current_map]:
        map_textures[current_map][texture] = load(map_textures[current_map][texture])

for current_player in player_textures:
    player_textures[current_player] = load(player_textures[current_player], pixel_size=6)

### Game State Variables ###
mapBlocks = [blocks.Block((width/2 - 32 * PIXEL_SIZE, height/2, 64 * PIXEL_SIZE, PIXEL_SIZE)), 
             blocks.Block((width/2 - 31 * PIXEL_SIZE, height/2 + PIXEL_SIZE, 62 * PIXEL_SIZE, PIXEL_SIZE * 3)),
             blocks.Block((width/2 - 29 * PIXEL_SIZE, height/2 + PIXEL_SIZE * 4, 58 * PIXEL_SIZE, PIXEL_SIZE * 2)),
             blocks.Block((width/2 - 24 * PIXEL_SIZE, height/2 + PIXEL_SIZE * 6, 48 * PIXEL_SIZE, PIXEL_SIZE * 2)),]
players = [player.Player((width/2 - 150, 100), (255, 50, 50), [K_w, K_a, K_s, K_d], bullets.Bullet, "orange", player_textures["orange"]), player.Player((width/2 + 150, 100), (50, 255, 50), [K_UP, K_LEFT, K_DOWN, K_RIGHT], bullets.Bullet, "duck", player_textures["duck"])]
bulletList = []

def textCentered(msg, x, y, size, color):
    font = pygame.font.SysFont("Segoe UI Black", size)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def drawMap():
    screen.blit(map_textures["grassy"]["main"], (width/2 - (32 * PIXEL_SIZE), height/2 - (3 * PIXEL_SIZE)))

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        if e.type == VIDEORESIZE:
            width, height = e.w, e.h

        if e.type == KEYDOWN:
            inputs[e.key] = True
            if e.key in inputTime and pygame.time.get_ticks() - inputTime[e.key] < DOUBLE_STROKE_TICK:
                doubleInput[e.key] = True
            else:
                inputTime[e.key] = pygame.time.get_ticks()

            ### FOR DEVELOPMENT - REMOVE LATER ###
            if e.key == K_ESCAPE:
                running = False

        elif e.type == KEYUP and e.key in inputs:
            del inputs[e.key]
    
    screen.fill(BACKGROUND)
    
    drawMap()

    for bullet in bulletList:
        bullet.draw(screen)
        bullet.update()

    for n, p in enumerate(players):
        p.draw(screen)
        p.update(mapBlocks, inputs, doubleInput)
        p.handleBullets(inputs, bulletList)

        if(p.health <= 0):
            players.pop(n)
    
    if len(players) == 1:
        textCentered(f"{players[0].name} wins!", width/2, 300, 100, (0, 0, 0))

    remove = []
    for k in doubleInput:
        if doubleInput[k] == True:
            remove.append(k)
    for k in remove:
        del doubleInput[k]
        del inputTime[k]
            
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()