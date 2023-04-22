"""
Bring together model, view, and controller to implement Parcel B Beetle Quest. 
"""
import sys
import pygame
from pygame.locals import *
from character import PlayerCharacter
from scene import MapScene, EventScene

pygame.init()
pygame.display.set_caption("Parcel B: Beetle Quest")

# Define constants related to pygame window
HEIGHT = 500
WIDTH = 800
FPS = 60

# Define constant filepaths in relation to project directory
PLAYER_SPRITE_FILEPATH = "data/sprite_data/resting.png"

# Setup pygame clock
FramePerSec = pygame.time.Clock()

# Define surface to draw on and sprites
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
displaysurface.fill((0, 0, 0))
player = PlayerCharacter(PLAYER_SPRITE_FILEPATH)
player.update_inventory("coat")
player.update_inventory("shtuff")

map = MapScene(displaysurface, player)
map.draw(0)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
