import pygame
from random import randint
from settings import *

def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "img": imagen}


def create_player(imagen:pygame.Surface = None, left=0, top=0, width=10, height=10):
    return create_block(imagen,left, top, width, height)


def create_traffic(imagen:pygame.Surface = None, width=50, height=50):
    return create_block(imagen, randint(centrar_road, limte_x_road - player_w), aparecer_arriba, width, height)

def create_powerup(imagen:pygame.Surface = None, width=20, height=20):
    return create_block(imagen, randint(centrar_road, limte_x_road - player_w), aparecer_arriba, width, height)

def create_danger(imagen:pygame.Surface = None, width=20, height=20):
    return create_block(imagen, randint(centrar_road, limte_x_road - player_w), aparecer_arriba, width, height)

# def create_powerup(imagen:pygame.Surface = None, left=0, top=0, width=powerup_w, height=powerup_h, dir=0, color=YELLOW, borde=0, radio= powerup_w // 2):
#      if imagen:
#         imagen = pygame.transform.scale(imagen, (width, height))
#      return {"rect": pygame.Rect(randint(centrar_road, limte_x_road - player_w), aparecer_arriba, width, height), "color": color, "dir": dir, "borde": borde, "radio": radio}


