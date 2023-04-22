import sys
import pygame
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 500
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60

MAP_BACKGROUND_FILEPATH = "data/scene_data/map1.png"

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))

    map_background = pygame.image.load(MAP_BACKGROUND_FILEPATH)

    displaysurface.blit(map_background, (-700, -300))

    font = pygame.font.Font("freesansbold.ttf", 20)
    white = (255, 255, 255)
    blue = (0, 0, 100)
    text = font.render("Choose direction", True, white, blue)
    textRect = text.get_rect()
    textRect.topleft = (100, 100)
    displaysurface.blit(text, textRect)

    pygame.display.update()
    FramePerSec.tick(FPS)
