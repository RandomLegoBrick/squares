BACKGROUND = (245, 250, 255)
GRAVITY = 1
PIXEL_SIZE = 16
DOUBLE_STROKE_TICK = 250
PLAYER_SIZE = 48
FPS_TARGET = 120
WIDTH, HEIGHT = 1920*2, 1080*2

## Temp
PLAYER1 = "orange"
PLAYER2 = "blueberry"

map_textures = {
    "grassy" : {
        "main" : "assets/maps/grassy/main_platform.png",
        "secondary" : "assets/maps/grassy/secondary_platform.png",
        "background" :  "assets/maps/grassy/background.png",
    }
}

player_textures = {
    "duck" : "assets/players/duck.png",
    "blueberry" : "assets/players/blueberry.png",
    "red" : "assets/players/red.png",
    "orange" : "assets/players/orange.png",
    "flamey" : "assets/players/flamey.png",
}
player_effects = {
    "dash" : "assets/players/effects/dash.png",
}

weapon_textures = {
    "bullet_standard" : "assets/weapons/bullets/bullet_standard.png",
    "grenade_standard" : "assets/weapons/grenades/grenade_standard.png",
}

explosion_textures = [
    "assets/weapons/effects/explosion_0.png",
]

BULLET_STAT_TABLE = {
    "bullet_standard" : {
        "velocity" : 50,
        "damage" : 5,
        "reload" : 10,
    },
    "bullet_heavy" : {
        "velocity" : 20,
        "damage" : 15,
        "reload" : 30,
    },
    "bullet_light" : {
        "velocity" : 80,
        "damage" : 2,
        "reload" : 5,
    },
    "grenade_standard" : {
        "velocity" : 10,
        "damage" : 60
    }
}