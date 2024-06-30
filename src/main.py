import pygame
from settings import *
from bloques import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()
running = True

# Cargar imagenes
road_image = pygame.image.load("./src/assets/road.jpg")
road_image = pygame.transform.scale(road_image, (road_w, road_h))

red_car_image = pygame.image.load("./src/assets/red-car.png") #poner .convert() para ver lo que ocupa el auto.

# Creo el jugador
player_block = create_player(red_car_image, CENTER_X - player_w // 2, CENTER_Y - player_h // 2)

#mover jugador
move_left = False
move_right = False
move_up = False
move_down = False

while running:
    clock.tick(FPS)
    #       ----> detectar los eventos <----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #coordenadas del mouse:
        print(pygame.mouse.get_pos())

        # mover autito
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
                move_right = False
            if event.key == pygame.K_RIGHT:
                move_right = True
                move_left = False
            if event.key == pygame.K_UP:
                move_up = True
                move_down = False
            if event.key == pygame.K_DOWN:
                move_down = True
                move_up = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_down = False
        # FIN mover autito

    #       ----> FIN detectar los eventos <----


    #       ----> actualizar los elementos <----
    # ilusion de scroll de la ruta
    road_y += scroll_speed  # movemos la posicion Y de la calle
    if road_y >= road_h:  
        road_y = 0  # cuando llege al final, la imagen aparece de nuevo en Y=0 simulando movimiento

    # Mover el jugador
    print(player_block["rect"].x, player_block["rect"].y)
    if move_left and player_block["rect"].left > centrar_road - player_w:
        player_block["rect"].x -= SPEED
    if move_right and player_block["rect"].right < limte_x_road + player_w:
        player_block["rect"].x += SPEED
    if move_up and player_block["rect"].top > 20:
        player_block["rect"].y -= SPEED
    if move_down and player_block["rect"].bottom < HEIGHT - 20:
        player_block["rect"].y += SPEED

    #si toco el pasto, me freno
    if player_block["rect"].left < centrar_road:
        move_up = False
        player_block["rect"].y += SPEED
    if player_block["rect"].right > limte_x_road:
        move_down = False
        player_block["rect"].y += SPEED

    #       ----> FIN actualizar los elementos <----



    #       ----> dibujar elementos en pantalla <----
    screen.fill(GREEN)
        
    # Dibujar la calle en la pantalla
    screen.blit(road_image, (centrar_road, road_y))  # dibujo la calle por primera vez
    screen.blit(road_image, (centrar_road, road_y - road_h))  # dibujo la imagen de nuevo con el movimiento de la calle

    # pygame.draw.rect(screen, RED, player_block["rect"]) 
    screen.blit(player_block["img"], (player_block["rect"].x, player_block["rect"].y)) # autito player

                          
    pygame.display.flip() # actualiza la pantalla

    #       ----> FIN dibujar elementos en pantalla <----

pygame.quit()