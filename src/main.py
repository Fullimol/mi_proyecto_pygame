import pygame
from settings import *
from bloques import *
from colisiones import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()
running = True

# Cargar imagenes
road_image = pygame.image.load("./src/assets/road.jpg")
road_image = pygame.transform.scale(road_image, (road_w, road_h))

                                                             # QUITAR EL CONVERT() PARA ELIMINAR LOS FONDOS NEGROS.
red_car_image = pygame.image.load("./src/assets/red-car.png")
blue_car_image = pygame.image.load("./src/assets/blue-car.png")
van_car_image = pygame.image.load("./src/assets/van-car.png")

# Creo el jugador
player_block = create_player(red_car_image, CENTER_X - player_w // 2, CENTER_Y - player_h // 2)

# creo autito de trafico
blue_car_block = create_traffic(blue_car_image, width=blue_car_w, height=blue_car_h)

############ (!) SOLUCIONAR que la van aparece en el mismo punto que el auto azul, se superponen   ###########
# van_car_block = create_traffic(van_car_image, width=van_car_w, height=van_car_h)                 

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

    if player_block["rect"].top > HEIGHT:
        print("PERDISTE!")


    # mover el autito de trafico
    blue_car_block["rect"].y += traffic_speed
    if blue_car_block["rect"].top > HEIGHT:
        # resetear el autito de trafico
        blue_car_block["rect"].x = randint(centrar_road, limte_x_road - player_w)
        blue_car_block["rect"].y = aparecer_arriba

    # van_car_block["rect"].y += traffic_speed
    # if van_car_block["rect"].top > HEIGHT:
    #     # resetear el autito de trafico
    #     van_car_block["rect"].x = randint(centrar_road, limte_x_road - player_w)
    #     van_car_block["rect"].y = aparecer_arriba

    # Detectar si chocamos:
    if detectar_colision(player_block["rect"], blue_car_block["rect"]):
        print("Chocaste!")
        move_up = False
        player_block["rect"].y += reduce_speed

        # # Determinar la dirección del movimiento de separación al chocar por laterales a otro auto.
        # if player_block["rect"].right > blue_car_block["rect"].left and player_block["rect"].left < blue_car_block["rect"].left:
        #     # Colisión por la derecha del jugador
        #     player_block["rect"].right = blue_car_block["rect"].left
        # elif player_block["rect"].left < blue_car_block["rect"].right and player_block["rect"].right > blue_car_block["rect"].right:
        #     # Colisión por la izquierda del jugador
        #     player_block["rect"].left = blue_car_block["rect"].right
        # elif player_block["rect"].top < blue_car_block["rect"].bottom and player_block["rect"].bottom > blue_car_block["rect"].bottom:
        #     # Colisión por la parte superior del jugador
        #     move_up = False
        #     player_block["rect"].y += SPEED
            
    

    #       ----> FIN actualizar los elementos <----



    #       ----> dibujar elementos en pantalla <----
    screen.fill(GREEN)
        
    # Dibujar la calle en la pantalla
    screen.blit(road_image, (centrar_road, road_y))  # dibujo la calle por primera vez
    screen.blit(road_image, (centrar_road, road_y - road_h))  # dibujo la imagen de nuevo con el movimiento de la calle

    

    # pygame.draw.rect(screen, BLUE, player_block["rect"]) 
    screen.blit(player_block["img"], (player_block["rect"].x, player_block["rect"].y, player_w, player_h)) # autito player

    screen.blit(blue_car_block["img"], (blue_car_block["rect"].x, blue_car_block["rect"].y, player_w, player_h))
    # screen.blit(van_car_block["img"], (blue_car_block["rect"].x, blue_car_block["rect"].y, player_w, player_h))


                          
    pygame.display.flip() # actualiza la pantalla

    #       ----> FIN dibujar elementos en pantalla <----

pygame.quit()