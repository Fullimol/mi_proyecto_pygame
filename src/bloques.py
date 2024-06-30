import pygame
from random import randint
from settings import *

def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "img": imagen}


def create_player(imagen:pygame.Surface = None, left=0, top=0):
    return create_block(imagen,left, top, player_w, player_h)


def create_traffic(imagen:pygame.Surface = None, width=50, height=50):
    return create_block(imagen, randint(centrar_road, limte_x_road - player_w), aparecer_arriba, width, height)

# def create_traffic(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50):
#     return create_block(imagen, left, top, width, height)