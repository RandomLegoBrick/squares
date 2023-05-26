## Work In Progress
A smash-bros-esque fighting game writen in python using pygame. Name will change once I come up with a better one :P

## Instructions
*Note: these are subject to change as the project evolves*

## Running
make sure you have python and pygame installed first

```
git clone https://github.com/RandomLegoBrick/squares.git
cd squares
python main.py
```




## Playing the game
Player 1: 
- `WAD` to move 
- Double tap `W` or `D` to dash
- Press `S` to shoot
- Double tap `S` to throw grenade

Player 2: Arrow Keys to move
- Double tap `Left` or `Right` to dash
- Press `Down` to shoot
- Double tap `Down` to throw grenade

## Player Skins
Current possible skins: (As of now, skins can be changed on lines 59-63 of `main.py`)
- red
- blueberry
- orange
- flamey
- duck

## Adding more players
Players can be added by copy/pasting the following code into the `players` list located on line 59 of main.py.

`player.Player((WIDTH/2, HEIGHT/2 - 50), [K_i, K_j, K_k, K_l], "flamey"),`

The first argument is a tuple containing the player's x and y cordinates. The second arument is a list containing the keymap for the players in the order "UP, LEFT, DOWN, RIGHT". The final argument is they player's skin which can be any of the values in the **Player Skins** section.


Todo (Will add more over time):
- Gameplay
    - [x] Movement
    - [x] Collisions
    - [x] Bullets
    - [x] Screen Shake
    - [ ] Knockback
    - [ ] Dash & Jump animations
    - [x] Camera
    - [x] Paralax Background
- Art
    - Map: Grassy
        - [x] Main Island
        - [ ] Secondary Islands
        - [ ] Background
    - Players
        - [x] Blueberry
        - [x] Red
        - [x] Orange
        - [x] flamey
        - [ ] Controller
        - Think of more...
    - Weapons
        - [x] basic gun
        - [x] grenade
    - Menu Art
- Menus
    - [ ] Main Menu
    - [ ] Game Setup
    - [ ] Game Over
    - [ ] Manual