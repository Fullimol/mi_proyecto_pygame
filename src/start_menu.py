import pygame
from settings import *
from bloques import *
from colisiones import *
from modulos import *

def start_menu_screen(screen, high_score, select_sound, menu_background, fuente, fuente_2):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SIZE_SCREEN)
    pygame.display.set_caption("Furious Road")
    pygame.display.set_icon(pygame.image.load("./src/assets/images/icon.png"))

    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        mostrar_texto(screen, (CENTER_X, 100), "xxx FURIOUS ROAD xxx", fuente, MAGENTA)
        if high_score != 0:
            mostrar_texto(screen, (CENTER_SCREEN), f"High Score    {high_score}", fuente, MAGENTA)
        mostrar_texto(screen, (CENTER_X, 500), "SPACE to start", fuente_2, MAGENTA)
        pygame.display.flip()
        wait_user(pygame.K_SPACE, select_sound)

        running = False