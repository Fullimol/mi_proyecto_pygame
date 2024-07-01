import pygame
from settings import *
from bloques import *
from colisiones import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()
running = True

lista_imagenes = []

NEWPOWERUPEVENT = pygame.USEREVENT + 1
NEWDANGERHOLE = pygame.USEREVENT + 2
pygame.time.set_timer(NEWPOWERUPEVENT, 5000)
pygame.time.set_timer(NEWDANGERHOLE, 6000)

# Cargar imagenes
road_image = pygame.image.load("./src/assets/road.jpg")
road_image = pygame.transform.scale(road_image, (road_w, road_h))

                                                             # QUITAR o poner EL CONVERT() PARA VER LOS FONDOS NEGROS.
red_car_image = pygame.image.load("./src/assets/red-car.png")
blue_car_image = pygame.image.load("./src/assets/blue-car.png")
health_powerup_image = pygame.image.load("./src/assets/health.png")
health_powerup_image = pygame.transform.scale(health_powerup_image, (45, 45))
danger_hole_image = pygame.image.load("./src/assets/hole.png")
danger_hole_image = pygame.transform.scale(danger_hole_image, (100, 100))

# Creo el jugador
player_block = create_player(red_car_image, CENTER_X - player_w // 2, CENTER_Y - player_h // 2)
# creo autito de trafico
blue_car_block = create_traffic(blue_car_image, width=blue_car_w, height=blue_car_h)
# power_up_healt
power_up_healt = create_powerup(health_powerup_image, width=powerup_w, height=powerup_h)
# mostrar conos
danger_hole = create_powerup(danger_hole_image, width=danger_hole_w, height=danger_hole_h)

#mover jugador
move_left = False
move_right = False
move_up = False
move_down = False

# configuro la fuente del texto
fuente = pygame.font.SysFont(None, 48)
score = 0
health = 100

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

    # CREAR POWERUP
        if event.type == NEWPOWERUPEVENT:
            power_up_healt = create_powerup()

        if event.type == NEWDANGERHOLE:
            danger_hole = create_powerup()

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
        player_block["rect"].y += SPEED + 1
    if player_block["rect"].right > limte_x_road:
        move_down = False
        player_block["rect"].y += SPEED + 1

    # mover el autito de trafico
    blue_car_block["rect"].y += traffic_speed
    if blue_car_block["rect"].top > HEIGHT:
        # resetear el autito de trafico
        blue_car_block["rect"].x = randint(centrar_road, limte_x_road - player_w)
        blue_car_block["rect"].y = aparecer_arriba
    power_up_healt["rect"].y += SPEED
    danger_hole["rect"].y += scroll_speed
    

    # Detectar si chocamos con el trafico
    if detectar_colision(player_block["rect"], blue_car_block["rect"]):
        move_up = False
        player_block["rect"].y += reduce_speed
        health -= 1
    
    # Detectar si chocamos con el powerup
    if detectar_colision(player_block["rect"], power_up_healt["rect"]):
        power_up_healt["rect"].y = 700
        health += 50
        if health > 100:
            health = 100

    # Detectar si chocamos con los conos
    if detectar_colision(player_block["rect"], danger_hole["rect"]):
        move_up = False
        player_block["rect"].y += reduce_speed
        health -= 1
        
    # Detectamos si perdimos y cerrar juego:
    if health <= 0 or player_block["rect"].top > HEIGHT:
        running = False

    # Incrementar el puntaje
    score += 1
    #       ----> FIN actualizar los elementos <----


    #       ----> dibujar elementos en pantalla <----
    screen.fill(GREEN)
        
    # Dibujar la calle en la pantalla
    screen.blit(road_image, (centrar_road, road_y))  # dibujo la calle por primera vez
    screen.blit(road_image, (centrar_road, road_y - road_h))  # dibujo la imagen de nuevo con el movimiento de la calle

    # Dibujar el autitos en la pantalla
    screen.blit(player_block["img"], (player_block["rect"].x, player_block["rect"].y, player_w, player_h)) # autito player
    screen.blit(blue_car_block["img"], (blue_car_block["rect"].x, blue_car_block["rect"].y, player_w, player_h))

    #Mostrar powerup
    # pygame.draw.rect(screen, RED, power_up_healt["rect"], border_radius=powerup_w // 2)
    screen.blit(health_powerup_image, (power_up_healt["rect"].x, power_up_healt["rect"].y))

    #Mostrar danger hole
    screen.blit(danger_hole_image, (danger_hole["rect"].x, danger_hole["rect"].y))

    # Dibujar el puntaje en la pantalla
    score_text = fuente.render(f'Score: {score}', False, BLACK)
    healt_text = fuente.render(f'Health:% {health}', True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(healt_text, (10, 50))
                          
    pygame.display.flip() # actualiza la pantalla
    #       ----> FIN dibujar elementos en pantalla <----


print("Juego finalizado.")

pygame.quit()