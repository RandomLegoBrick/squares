import pygame
from pygame.locals import *
from modules.constants import *
from modules import player, blocks, bullets
from modules.functions import *
import random, time

### Enviornment Variables ###
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption("bytelash")
SCREEN_WIDTH, SCREEN_HEIGHT = window.get_size()
clock = pygame.time.Clock()
running = True
screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()



### Input Variables ###
inputs = {}
inputTime = {} # Stores the time of the last input for each key
doubleInput = {} # Keep track of double strokes
mouseX, mouseY = 0, 0
clicked = False
mouse = [pygame.SYSTEM_CURSOR_ARROW]
def setCursor(cursor):
    mouse[0] = cursor

### Load Textures ###
def load(path, pixel_size=PIXEL_SIZE):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (img.get_width() * pixel_size, img.get_height() * pixel_size))
    return img.convert_alpha()

for current_map in map_textures:
    for texture in map_textures[current_map]:
        map_textures[current_map][texture] = load(map_textures[current_map][texture], pixel_size=PIXEL_SIZE)

for current_player in player_textures:
    player_textures[current_player] = load(player_textures[current_player], pixel_size=6)

for current_weapon in weapon_textures:
    weapon_textures[current_weapon] = load(weapon_textures[current_weapon], pixel_size=6)

for current_item in ui_textures:
    ui_textures[current_item] = load(ui_textures[current_item], pixel_size=8)


scene = "menu"

### Camera ###
class camera():
    x = 0
    y = 0
    shake = 0


### Game State Variables ###
bulletList = []
grenadeList = []

bullets.init(weapon_textures)
player.init(player_effects, player_textures, camera, bulletList, grenadeList)

mapBlocks = [blocks.Block((WIDTH/2 - 32 * PIXEL_SIZE, HEIGHT/2, 64 * PIXEL_SIZE, PIXEL_SIZE)), 
             blocks.Block((WIDTH/2 - 31 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE, 62 * PIXEL_SIZE, PIXEL_SIZE * 3)),
             blocks.Block((WIDTH/2 - 29 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE * 4, 58 * PIXEL_SIZE, PIXEL_SIZE * 2)),
             blocks.Block((WIDTH/2 - 24 * PIXEL_SIZE, HEIGHT/2 + PIXEL_SIZE * 6, 48 * PIXEL_SIZE, PIXEL_SIZE * 2)),
             blocks.Block((WIDTH/2-(16 * PIXEL_SIZE) - PIXEL_SIZE*55, HEIGHT/2-(10 * PIXEL_SIZE), PIXEL_SIZE*32, PIXEL_SIZE*5)),
             
             #right island
             blocks.Block((WIDTH/2-(14 * PIXEL_SIZE) + PIXEL_SIZE*35, HEIGHT/2-(6 * PIXEL_SIZE) - PIXEL_SIZE*15, PIXEL_SIZE * 28, PIXEL_SIZE*3)),
             blocks.Block((WIDTH/2-(14 * PIXEL_SIZE) + PIXEL_SIZE*37, HEIGHT/2-(6 * PIXEL_SIZE) - PIXEL_SIZE*14, PIXEL_SIZE * 23, PIXEL_SIZE)),
             ]  

## Edit player stuff here ##
players = [player.Player((WIDTH/2 - 150, HEIGHT/2 - 50), [K_w, K_a, K_s, K_d], "orange"), 
           player.Player((WIDTH/2 + 150, HEIGHT/2 - 50), [K_UP, K_LEFT, K_DOWN, K_RIGHT], "duck"),
           # Add Players here v
           player.Player((WIDTH/2, HEIGHT/2 - 50), [K_i, K_j, K_k, K_l], "flamey"),
           # Add Players here ^
           ]



def textCentered(screen, msg, x, y, size, color):
    font = pygame.font.Font("assets/UI/fonts/pixel/Pixel.ttf", size)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def drawMap():
    screen.blit(map_textures["grassy"]["main"], (WIDTH/2-(32 * PIXEL_SIZE), HEIGHT/2-(3 * PIXEL_SIZE)))
    screen.blit(map_textures["grassy"]["secondary"], (WIDTH/2-(16 * PIXEL_SIZE) - PIXEL_SIZE*55, 
                                                      HEIGHT/2-(10 * PIXEL_SIZE) - PIXEL_SIZE*10))
    screen.blit(map_textures["grassy"]["right"], (WIDTH/2-(14 * PIXEL_SIZE) + PIXEL_SIZE*35, 
                                                      HEIGHT/2-(6 * PIXEL_SIZE) - PIXEL_SIZE*20))


## Handle Game Scene
def runGame(dt):
    window.blit(map_textures["grassy"]["background"], ((WIDTH/2)-(128 * PIXEL_SIZE) + camera.x/5, 
                                                       (HEIGHT/2)-(64 * PIXEL_SIZE) + camera.y/5))
    #window.blit(map_textures["grassy"]["background_layer2"], ((WIDTH/2)-(64 * PIXEL_SIZE) + camera.x/5, 
    #                                                   (HEIGHT/2)-(48 * PIXEL_SIZE) + camera.y/5))
    screen.fill([0, 0, 0, 0])
    
    
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
        textCentered(screen, f"{players[0].name} wins!", WIDTH/2, HEIGHT/2 - 300, 100, (0, 0, 0))

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
    cameraFollowing = 0
    for p in players:
        if dist(p.x, p.y, WIDTH/2, HEIGHT/2) < 2000:
            playerPos[0] += p.x
            playerPos[1] += p.y
            cameraFollowing += 1

    if cameraFollowing: 

        playerPos = [playerPos[0]/cameraFollowing, playerPos[1]/cameraFollowing]
    
        camera.shake = int(camera.shake)
        camera.x = lerp(camera.x, -playerPos[0] + SCREEN_WIDTH/2, 0.1) + random.randint(-camera.shake, camera.shake)
        camera.y = lerp(camera.y,  -playerPos[1] + SCREEN_HEIGHT/2, 0.1) + random.randint(-camera.shake, camera.shake)

    else:
        camera.x = lerp(camera.x, -SCREEN_WIDTH/2, 0.1)
        camera.y = lerp(camera.y, -SCREEN_HEIGHT/2, 0.1)

    
    if len(players) == 0:
        global scene
        scene = "menu"

        for p in players:
            p.reset()

    camera.shake = clamp(camera.shake - 0.1, 0, 20)

    window.blit(screen, (camera.x, camera.y))

def button(screen, x, y, w, h, txt):
    hover = 0
    if mouseX > x and mouseX < x + w and mouseY > y and mouseY < y + h:
        hover = 1
        setCursor(pygame.SYSTEM_CURSOR_HAND)
        
    
    pygame.draw.rect(screen, (200, 200, 200), (x, y, w, h))
    pygame.draw.rect(screen, (220, 220, 220), (x - (5-hover*3), y - (5-hover*3), w, h))
    textCentered(screen, txt, x + w/2, y + h/2 - (5-hover*3), 48, (0, 0, 0))

    return hover > 0 and clicked

class playerLoadout():
    def __init__(self, x, y, keyset, num):
        self.x = x
        self.y = y
        self.keyset = keyset
        self.num = num
    
    def draw(self, screen):
        textCentered(screen, "Player "+str(self.num), self.x, self.y, 24, (0, 0, 0))

playerLoadouts = [
    playerLoadout(100, 200, [K_w, K_a, K_s, K_d], 1)
]

## Handle Menu Scene
def runMenu():
    window.blit(map_textures["grassy"]["background"], ((SCREEN_WIDTH/2)-(128 * PIXEL_SIZE), (SCREEN_HEIGHT/2)-(50 * PIXEL_SIZE)))
    
    ## TITLE
    textCentered(window, "BYTELASH", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200 - 5, 72, (0, 0, 0))
    textCentered(window, "BYTELASH", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200 + 5, 72, (0, 0, 0))
    textCentered(window, "BYTELASH", SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2 - 200, 72, (0, 0, 0))
    textCentered(window, "BYTELASH", SCREEN_WIDTH/2 + 5, SCREEN_HEIGHT/2 - 200, 72, (0, 0, 0))
    textCentered(window, "BYTELASH", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200, 72, (255, 255, 255))

    ## Player Setup
    for pl in playerLoadouts:
        pl.draw(window)

    window.blit(map_textures["grassy"]["left"], (SCREEN_WIDTH/2 - 16*PIXEL_SIZE, SCREEN_HEIGHT/2 - 150))

    if button(window, SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 150, 300, 100, "Play"):
        global scene
        scene = "game"

## Variables for movement compensation
prev_time = time.time()
startTime = time.time()

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
        elif e.type == MOUSEBUTTONUP:
            clicked = True
        elif e.type == MOUSEMOTION:
            mouseX = e.pos[0]
            mouseY = e.pos[1]
    
    if scene == "game":
        runGame(dt)
    elif scene == "menu":
        runMenu()
    
    pygame.mouse.set_cursor(mouse[0])
    setCursor(pygame.SYSTEM_CURSOR_ARROW)
    pygame.display.flip()
    clock.tick(FPS_TARGET)
    clicked = False

pygame.quit()