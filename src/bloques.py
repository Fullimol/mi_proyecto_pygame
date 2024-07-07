import pygame
from random import randint
from settings import *

def create_block(imagen:pygame.Surface = None, left=0, top=0, width=50, height=50):
    """ Crea un rectangulo

    Args:
        imagen (pygame.Surface, optional): Pasamos la imagen a mostrar en el rectangulo.
        left (int, optional): pasamos la coordenada X donde inicia el rectangulo.
        top (int, optional): pasamos la coordenada Y donde inicia el rectangulo.
        width (int, optional): pasamos el ancho del rectangulo.
        height (int, optional): pasamos el alto del rectangulo.

    Returns:
        dict: crea un rectangulo en forma de diccionario
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    return {"rect": pygame.Rect(left, top, width, height), "img": imagen}

def create_player(imagen:pygame.Surface = None, left=0, top=0, width=10, height=10):
    return create_block(imagen,left, top, width, height)

def create_traffic(imagen:pygame.Surface = None, width=50, height=50):
    return create_block(imagen, randint(road_left, road_right - player_w), aparecer_arriba, width, height)

def create_powerup(imagen:pygame.Surface = None, width=20, height=20):
    return create_block(imagen, randint(road_left, road_right - player_w), aparecer_arriba, width, height)

def create_danger(imagen:pygame.Surface = None, width=20, height=20):
    return create_block(imagen, randint(road_left, road_right - player_w), aparecer_arriba, width, height)