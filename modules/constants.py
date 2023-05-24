BACKGROUND = (255, 255, 255)
GRAVITY = 1
PIXEL_SIZE = 16
DOUBLE_STROKE_TICK = 200
PLAYER_SIZE = 48

map_textures = {
    "grassy" : {
        "main" : "assets/maps/grassy/main_platform.png",
    }
}

player_textures = {
    "duck" : "assets/players/duck.png",
    "blueberry" : "assets/players/blueberry.png",
    "red" : "assets/players/red.png",
    "orange" : "assets/players/orange.png",
}

BULLET_STAT_TABLE = {
    "standard" : {
        "velocity" : 50,
        "damage" : 5,
        "reload" : 10,
    },
    "heavy" : {
        "velocity" : 20,
        "damage" : 15,
        "reload" : 30,
    },
    "light" : {
        "velocity" : 80,
        "damage" : 2,
        "reload" : 5,
    }
}