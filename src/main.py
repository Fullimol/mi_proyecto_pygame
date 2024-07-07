import pygame
from settings import *
from bloques import create_player, create_danger, create_powerup, create_traffic
from colisiones import detectar_colision
from modulos import load_json, save_data, cargar_sonido, escalar_imagenes, terminar, mostrar_texto, wait_user
from start_menu import start_menu_screen
from random import randint

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Furious Road")
pygame.display.set_icon(pygame.image.load("./src/assets/images/icon.png"))
clock = pygame.time.Clock()

#cargar json con los recursos:
recursos = load_json("./recursos.json")

# Cargar sonidos
music_race = cargar_sonido(recursos["sounds"]["music_race"], 0.1)
healt_sound = cargar_sonido(recursos["sounds"]["healt_sound"], 0.07)
motor_carFX = cargar_sonido(recursos["sounds"]["motor_carFX"], 0.09)
select_sound = cargar_sonido(recursos["sounds"]["select_sound"], 0.05)
game_over_sound = cargar_sonido(recursos["sounds"]["game_over_sound"], 0.05)
hornFX = cargar_sonido(recursos["sounds"]["hornFX"], 0.05)


# Cargar imagenes
traffic_cars_images = [
    escalar_imagenes(recursos["images"]["traffic_cars"][0], traffic_car_w, traffic_car_h),
    escalar_imagenes(recursos["images"]["traffic_cars"][1], traffic_car_w, traffic_car_h),
    escalar_imagenes(recursos["images"]["traffic_cars"][2], traffic_car_w, traffic_car_h),
    escalar_imagenes(recursos["images"]["traffic_cars"][3], traffic_car_w, traffic_car_h),
    escalar_imagenes(recursos["images"]["traffic_cars"][4], traffic_car_w, traffic_car_h),
    escalar_imagenes(recursos["images"]["traffic_cars"][5], traffic_car_w, traffic_car_h)
]
red_car_image = escalar_imagenes(recursos["images"]["red_car"], player_w, player_h)
road_image = escalar_imagenes(recursos["images"]["road"], road_w, road_h)
tierra_image = escalar_imagenes(recursos["images"]["tierra"], tierra_w, tierra_h)
pasto_image = escalar_imagenes(recursos["images"]["pasto"], pasto_w, pasto_h)
health_powerup_image = escalar_imagenes(recursos["images"]["health_powerup"], powerup_w, powerup_h)
danger_hole_image = escalar_imagenes(recursos["images"]["danger_hole"], danger_hole_w, danger_hole_h)
menu_background = escalar_imagenes(recursos["images"]["menu_background"], WIDTH, HEIGHT)


# configuro la fuente del texto
fuente = pygame.font.Font(recursos["fonts"]["fuente1"], 75)
fuente_2 = pygame.font.SysFont(None, 48)


# creo eventos personalizados
NEWPOWERUPEVENT = pygame.USEREVENT + 1
NEWDANGERHOLE = pygame.USEREVENT + 2
pygame.time.set_timer(NEWPOWERUPEVENT, 5000)
pygame.time.set_timer(NEWDANGERHOLE, 3000)


high_score = 0
mov_horizontal_flag = True
music_on = True
while True:
    if music_on:
        music_race.play(loops=-1)

    #   --- Ventana de inicio ---
    start_menu_screen(screen, high_score, select_sound, menu_background, fuente, fuente_2)
    

    # --- Crear objetos en el mundo ---
    player_block = create_player(red_car_image, player_center_X, player_center_Y, player_w, player_h)
    traffic_car_block = create_traffic(traffic_cars_images[0], width=traffic_car_w, height=traffic_car_h)
    power_up_healt = create_powerup(health_powerup_image, width=powerup_w, height=powerup_h)
    danger_hole = create_danger(danger_hole_image, danger_hole_w, danger_hole_h)


    # Valores iniciales al iniciar la partida
    motor_carFX.play(loops=-1)
    score = 0
    health = 100
    move_left = False
    move_right = False
    move_up = False
    move_down = False


    running = True
    while running:
        clock.tick(FPS)
        #                                            ----> Detectar los eventos <----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            # mover autito
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = True
                    move_right = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = True
                    move_left = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = True
                    move_down = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = True
                    move_up = False
                # mutear musica.
                if event.key == pygame.K_m:
                    if music_on:
                        music_on = False
                        music_race.stop()
                    else:
                        music_on = True
                        music_race.play(loops=-1)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False
            # FIN mover autito

            # CREAR POWERUP y CONOS con el tiempo del evento
            if event.type == NEWPOWERUPEVENT:
                power_up_healt = create_powerup()

            if event.type == NEWDANGERHOLE:
                danger_hole = create_danger(danger_hole_image, danger_hole_w, danger_hole_h)
        #                                            ----> FIN detectar los eventos <----


        #                                            ----> Actualizar los elementos <----
        # Mover el powerup horizontalmente mientras cae.
        if mov_horizontal_flag:
            power_up_healt["rect"].x += healt_move_speed_x
            if power_up_healt["rect"].x >= road_right - powerup_w:
                mov_horizontal_flag = False
        else:
            power_up_healt["rect"].x -= healt_move_speed_x
            if power_up_healt["rect"].x <= road_left:
                mov_horizontal_flag = True

        # Ilusion de scroll de la ruta, tierra y pasto.
        road_top += scroll_speed  # movemos la POSICIÓN Y de la calle desde 0 a abajo
        if road_top >= road_h:  
            road_top = 0  # cuando llege al final, la imagen aparece de nuevo en Y=0 simulando movimiento

        tierra_top += scroll_speed
        if tierra_top >= tierra_h:
            tierra_top = 0

        pasto_top += scroll_speed
        if pasto_top >= pasto_h:
            pasto_top = 0

        # Mover el jugador verificando teclas y limitando los bordes
        if move_left and player_block["rect"].left > road_left - player_w:
            player_block["rect"].x -= SPEED
        if move_right and player_block["rect"].right < road_right + player_w:
            player_block["rect"].x += SPEED
        if move_up and player_block["rect"].top > 20:
            player_block["rect"].y -= SPEED
        if move_down and player_block["rect"].bottom < HEIGHT - 20:
            player_block["rect"].y += SPEED

        # Si toco el pasto, me freno
        if player_block["rect"].left < road_left:
            player_block["rect"].y += SPEED - 1
            move_up = False
            score -= 1
        if player_block["rect"].right > road_right:
            player_block["rect"].y += SPEED - 1
            move_up = False
            score -= 1

        # Mover el autito de trafico
        traffic_car_block["rect"].y += traffic_speed
        if traffic_car_block["rect"].top > HEIGHT:
            # cambiar imagen del auto de trafico
            traffic_car_block["img"] = traffic_cars_images[randint(0, len(traffic_cars_images) - 1)] # index aleatorio para cargar la img del auto
            # reseteo ubicacion del autito de trafico
            traffic_car_block["rect"].x = randint(road_left, road_right - traffic_car_w)
            traffic_car_block["rect"].y = aparecer_arriba
        power_up_healt["rect"].y += SPEED
        danger_hole["rect"].y += scroll_speed

        # Detectar si chocamos con el trafico
        if detectar_colision(player_block["rect"], traffic_car_block["rect"]):
            hornFX.play()
            move_up = False
            player_block["rect"].y += reduce_speed
            health -= 1
            score -= 1
        
        # Detectar si chocamos con el powerup
        if detectar_colision(player_block["rect"], power_up_healt["rect"]):
            healt_sound.play()
            power_up_healt["rect"].y = 700
            health += 20
            if health > 100:
                health = 100

        # Detectar si chocamos con los conos
        if detectar_colision(player_block["rect"], danger_hole["rect"]):
            hornFX.play()
            move_up = False
            player_block["rect"].y += reduce_speed 
            health -= 1
            
        # Detectamos si perdimos y terminar partida:
        if health <= 0 or player_block["rect"].top > HEIGHT:
            running = False

        # Incrementar el puntaje
        score += 1
        #                                            ----> FIN actualizar los elementos <----


        #                                            ----> Dibujar elementos en pantalla <----
        # dibujar paisaje:
        screen.blit(pasto_image, (pasto_left, pasto_top))
        screen.blit(pasto_image, (pasto_left, pasto_top - pasto_h))
        screen.blit(tierra_image, (tierra_left, tierra_top))
        screen.blit(tierra_image, (tierra_left, tierra_top - tierra_h))
        screen.blit(road_image, (road_left, road_top))  # dibujo la calle por primera vez
        screen.blit(road_image, (road_left, road_top - road_h))  # dibujo la imagen fuera de pantalla para simular movimiento

        # Dibujar objetos en el mundo.
        screen.blit(danger_hole_image, (danger_hole["rect"].x, danger_hole["rect"].y))
        # pygame.draw.rect(screen, BLACK, player_block["rect"])
        screen.blit(player_block["img"], (player_block["rect"].x, player_block["rect"].y, player_w, player_h))
        screen.blit(traffic_car_block["img"], (traffic_car_block["rect"].x, traffic_car_block["rect"].y, player_w, player_h))
        screen.blit(health_powerup_image, (power_up_healt["rect"].x, power_up_healt["rect"].y))

        # Dibujar el puntaje en la pantalla.
        if high_score != 0:
            mostrar_texto(screen, (100, 120), f"High: {high_score}", fuente_2, WHITE, BLACK)
        mostrar_texto(screen, (100, 80), f'Score: {score}', fuente_2, CYAN, BLACK)
        mostrar_texto(screen, (680 , 80), f'Healt % {health}', fuente_2, RED, BLACK)

        if music_on == False:
            mostrar_texto(screen, (100, 560), "Music OFF", fuente_2, WHITE, BLACK)
            
                            
        pygame.display.flip() # actualiza la pantalla
        #                                            ----> FIN dibujar elementos en pantalla <----

    # Pantalla GAME OVER
    motor_carFX.stop()
    game_over_sound.play()
    mostrar_texto(screen, (CENTER_X, 300), "GAME OVER", fuente, RED, BLACK)
    mostrar_texto(screen, (CENTER_X, 500), "SPACE to retry", fuente_2, RED, BLACK)
    pygame.display.flip()
    wait_user(pygame.K_SPACE, select_sound)
    

    if score > high_score:
        high_score = score
        save_data(high_score)

terminar()