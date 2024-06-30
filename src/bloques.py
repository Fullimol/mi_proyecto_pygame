import pygame
from random import randint
from settings import *

def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50, color=(255, 255, 255), dir=3, borde=0, radio=-1):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "color": color, "dir": dir, "borde": borde, "radio": radio, "img": imagen}

def create_player(imagen:pygame.Surface = None, left=0, top=0):
    return create_block(imagen,left, top, player_w, player_h, BLUE, radio = player_w // 2)