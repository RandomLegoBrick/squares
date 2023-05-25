import pygame
from pygame.locals import *
from modules.constants import *
from modules import player, blocks, bullets
from modules.functions import *
import random, time

### Enviornment Variables ###
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()


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
        map_textures[current_map][texture] = load(map_textures[current_map][texture], pixel_size=PIXEL_SIZE*2 if texture == "background" else PIXEL_SIZE)

for current_player in player_textures:
    player_textures[current_player] = load(player_textures[current_player], pixel_size=6)

for current_weapon in weapon_textures:
    weapon_textures[current_weapon] = load(weapon_textures[current_weapon], pixel_size=4)

### Camera ###
class camera():
    x = 0
    y = 0
    shake = 0

bullets.init(weapon_textures)
player.init(player_effects, player_textures, camera)



### Game State Variables ###
bulletList = []
grenadeList = []
mapBlocks = [blocks.Block((WIDTH/2 - 32 * PIXEL_SIZE, HEIGHT/2, 64 * PIXEL_SIZE, PIXEL_SIZE)), 
             blocks.Block((WIDTH/2 - 31 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE, 62 * PIXEL_SIZE, PIXEL_SIZE * 3)),
             blocks.Block((WIDTH/2 - 29 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE * 4, 58 * PIXEL_SIZE, PIXEL_SIZE * 2)),
             blocks.Block((WIDTH/2 - 24 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE * 6, 48 * PIXEL_SIZE, PIXEL_SIZE * 2)),]
players = [player.Player((WIDTH/2 - 150, 300), (255, 50, 50), [K_w, K_a, K_s, K_d], bulletList, grenadeList, PLAYER1), 
           player.Player((WIDTH/2 + 150, 300), (50, 255, 50), [K_UP, K_LEFT, K_DOWN, K_RIGHT], bulletList, grenadeList, PLAYER2)]


def textCentered(msg, x, y, size, color):
    font = pygame.font.SysFont("Segoe UI Black", size)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def drawMap():
    screen.blit(map_textures["grassy"]["main"], (WIDTH/2-(32 * PIXEL_SIZE), HEIGHT/2-(3 * PIXEL_SIZE)))

prev_time = time.time()
startTime = time.time()
xpos = 0

while running:
    # time dependancy
    now = time.time()
    dt = (now - prev_time) * 60
    prev_time = now
    

    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

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
    
    window.fill(BACKGROUND)
    screen.fill(BACKGROUND)
    
    drawMap()

    for bullet in reversed(bulletList):
        bullet.draw(screen)
        bullet.update(dt)
        if bullet.x > WIDTH*2 or bullet.x < -WIDTH or bullet.y > HEIGHT*2 or bullet.y < -HEIGHT:
            bulletList.remove(bullet)

    for n, p in enumerate(players):
        p.draw(screen, dt)
        p.update(mapBlocks, inputs, doubleInput, dt)
        p.handleBullets(inputs, doubleInput, dt)

        if(p.health <= 0):
            players.pop(n)
    
    if len(players) == 1:
        textCentered(f"{players[0].name} wins!", WIDTH/2, 300, 100, (0, 0, 0))

    for grenade in reversed(grenadeList):
        grenade.draw(screen)
        grenade.update(mapBlocks, camera, players, dt)
        if grenade.x > WIDTH*3 or grenade.x < -WIDTH or grenade.y > HEIGHT*2 or grenade.y < -HEIGHT or grenade.timer < 0:
            grenadeList.remove(grenade)

    remove = []
    for k in doubleInput:
        if doubleInput[k] == True:
            remove.append(k)
    for k in remove:
        del doubleInput[k]
        del inputTime[k]
    
    ## Get average position of all players
    playerPos = [0, 0]
    for p in players:
        playerPos[0] += p.x
        playerPos[1] += p.y
    playerPos = [playerPos[0]/len(players), playerPos[1]/len(players)]
    
    camera.shake = int(camera.shake)
    camera.x = lerp(camera.x, -playerPos[0] + WIDTH/2, 0.1) + random.randint(-camera.shake, camera.shake)
    camera.y = lerp(camera.y,  -playerPos[1] + HEIGHT/2, 0.1) + random.randint(-camera.shake, camera.shake)
    camera.shake = clamp(camera.shake - 0.1, 0, 20)

    window.blit(screen, (camera.x, camera.y))
    pygame.display.flip()
    clock.tick(FPS_TARGET)

pygame.quit()