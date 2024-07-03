import pygame
from settings import *
from bloques import *
from colisiones import *
import sys

##########  (!)   30/06  quitar/agregar los .convert() para sacar los fondos negros. HAY QUE CORREGIR LOS RECTANGULOS DE CADA BLOQUE  ##########

def terminar():
    pygame.quit()
    sys.exit()

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Furious Road")
pygame.display.set_icon(pygame.image.load("./src/assets/images/icon.png"))
clock = pygame.time.Clock()

NEWPOWERUPEVENT = pygame.USEREVENT + 1
NEWDANGERHOLE = pygame.USEREVENT + 2
pygame.time.set_timer(NEWPOWERUPEVENT, 5000)
pygame.time.set_timer(NEWDANGERHOLE, 3000)

# Cargar sonidos
music_race = pygame.mixer.Sound("./src/assets/sounds/music-race.mp3")
music_race.set_volume(0.1)
healt_sound = pygame.mixer.Sound("./src/assets/sounds/health.mp3")
healt_sound.set_volume(0.07)
motor_carFX = pygame.mixer.Sound("./src/assets/sounds/motorFX.mp3")
motor_carFX.set_volume(0.09)
music_race.play(loops=-1)
select_sound = pygame.mixer.Sound("./src/assets/sounds/select-sound.mp3")
select_sound.set_volume(0.05)
game_over_sound = pygame.mixer.Sound("./src/assets/sounds/finish-sound.mp3")
game_over_sound.set_volume(0.05)
hornFX = pygame.mixer.Sound("./src/assets/sounds/horn.mp3")
hornFX.set_volume(0.05)

# Cargar imagenes
def escalar_imagenes(imagen, width, height):
    return pygame.transform.scale(imagen, (width, height))

traffic_cars_images = [
    escalar_imagenes(pygame.image.load("./src/assets/images/blue-car.png"), traffic_car_w, traffic_car_h),
    escalar_imagenes(pygame.image.load("./src/assets/images/pink-car.png"), traffic_car_w, traffic_car_h),
    escalar_imagenes(pygame.image.load("./src/assets/images/van-car.png"), traffic_car_w, traffic_car_h),
    escalar_imagenes(pygame.image.load("./src/assets/images/green-car.png"), traffic_car_w, traffic_car_h),
    escalar_imagenes(pygame.image.load("./src/assets/images/yellow-car.png"), traffic_car_w, traffic_car_h),
    escalar_imagenes(pygame.image.load("./src/assets/images/white-car.png"), traffic_car_w, traffic_car_h)
]
road_image = pygame.image.load("./src/assets/images/road.jpg")
road_image = pygame.transform.scale(road_image, (road_w, road_h))
tierra_image = pygame.image.load("./src/assets/images/tierra.jpg")
tierra_image = pygame.transform.scale(tierra_image, (tierra_w, tierra_h))
pasto_image = pygame.image.load("./src/assets/images/pasto.jpg")
pasto_image = pygame.transform.scale(pasto_image, (pasto_w, pasto_h))
# QUITAR o poner EL CONVERT() PARA VER LOS FONDOS NEGROS.
red_car_image = pygame.image.load("./src/assets/images/red-car.png")
health_powerup_image = pygame.image.load("./src/assets/images/health.png")
health_powerup_image = pygame.transform.scale(health_powerup_image, (45, 45))
danger_hole_image = pygame.image.load("./src/assets/images/hole.png")
danger_hole_image = escalar_imagenes(danger_hole_image, danger_hole_w, danger_hole_h)
menu_background = pygame.image.load("./src/assets/images/background.jpg")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# configuro la fuente del texto
fuente = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 75)
fuente_2 = pygame.font.SysFont(None, 48)


def mostrar_texto(superficie:pygame.Surface, coordenada:tuple[int, int], texto:str, fuente:pygame.font.Font, color:tuple[int, int, int]= WHITE, background_color:tuple[int, int, int]= None ):
    sup_texto = fuente.render(texto , True, color, background_color)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenada
    superficie.blit(sup_texto, rect_texto)

def wait_user(tecla):
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == tecla:
                    select_sound.play()
                    flag_start = False

high_score = 0
mov_horizontal = True
while True:
    # Ventana de inicio
    screen.fill(GREEN)
    screen.blit(menu_background, (0, 0))

    mostrar_texto(screen, (CENTER_X, 100), "xxx FURIOUS ROAD xxx", fuente, MAGENTA)
    if high_score != 0:
        mostrar_texto(screen, (CENTER_SCREEN), f"High Score    {high_score}", fuente, MAGENTA)
    mostrar_texto(screen, (CENTER_X, 500), "SPACE to start", fuente_2, MAGENTA)
    pygame.display.flip()
    wait_user(pygame.K_SPACE)


    # Creo el jugador
    player_block = create_player(red_car_image, CENTER_X - player_w // 2, CENTER_Y - player_h // 2, player_w, player_h)
    # creo autito de trafico
    current_car_image_index = 0 # esto es para el cambio de imagen
    traffic_car_block = create_traffic(traffic_cars_images[current_car_image_index], width=traffic_car_w, height=traffic_car_h)
    # power_up_healt
    power_up_healt = create_powerup(health_powerup_image, width=powerup_w, height=powerup_h)
    # mostrar conos
    danger_hole = create_danger(danger_hole_image, danger_hole_w, danger_hole_h)

    motor_carFX.play(loops=-1)

    score = 0
    health = 100
    #mover jugador
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    running = True
    while running:
        clock.tick(FPS)

        #       ----> detectar los eventos <----

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

        # CREAR POWERUP
            if event.type == NEWPOWERUPEVENT:
                power_up_healt = create_powerup()

            if event.type == NEWDANGERHOLE:
                danger_hole = create_danger(danger_hole_image, danger_hole_w, danger_hole_h)

        #       ----> FIN detectar los eventos <----


        #       ----> actualizar los elementos <----

        if mov_horizontal:
            power_up_healt["rect"].x += healt_move_speed
            if power_up_healt["rect"].x >= limte_x_road - powerup_w:
                mov_horizontal = False
        else:
            power_up_healt["rect"].x -= healt_move_speed
            if power_up_healt["rect"].x <= centrar_road:
                mov_horizontal = True


        # ilusion de scroll de la ruta
        road_y += scroll_speed  # movemos la POSICIÓN Y de la calle desde 0 a abajo
        if road_y >= road_h:  
            road_y = 0  # cuando llege al final, la imagen aparece de nuevo en Y=0 simulando movimiento

        tierra_y += scroll_speed
        if tierra_y >= tierra_h:
            tierra_y = 0

        pasto_y += scroll_speed
        if pasto_y >= pasto_h:
            pasto_y = 0

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
            player_block["rect"].y += SPEED - 1
            move_up = False
            score -= 1
        if player_block["rect"].right > limte_x_road:
            player_block["rect"].y += SPEED - 1
            move_up = False
            score -= 1

        # mover el autito de trafico
        traffic_car_block["rect"].y += traffic_speed
        if traffic_car_block["rect"].top > HEIGHT:
            #cambiar imagen del auto de trafico
            current_car_image_index = (current_car_image_index + 1) % len(traffic_cars_images)
            traffic_car_block["img"] = traffic_cars_images[current_car_image_index]
            # reseteo ubicacion del autito de trafico
            traffic_car_block["rect"].x = randint(centrar_road, limte_x_road - player_w)
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
        #       ----> FIN actualizar los elementos <----


        #       ----> dibujar elementos en pantalla <----
        # screen.fill(GREEN)
        screen.blit(pasto_image, (pasto_x, pasto_y))
        screen.blit(pasto_image, (pasto_x, pasto_y - pasto_h))

        # dibujar tierra:
        # pygame.draw.rect(screen, BROWN, (148, 0, tierra_w, tierra_h))
        screen.blit(tierra_image, (tierra_x, tierra_y))
        screen.blit(tierra_image, (tierra_x, tierra_y - tierra_h))
            
        # Dibujar la calle en la pantalla
        screen.blit(road_image, (centrar_road, road_y))  # dibujo la calle por primera vez
        screen.blit(road_image, (centrar_road, road_y - road_h))  # dibujo la imagen de nuevo con el movimiento de la calle

        #Mostrar danger hole
        screen.blit(danger_hole_image, (danger_hole["rect"].x, danger_hole["rect"].y))

        # Dibujar el autitos en la pantalla
        # pygame.draw.rect(screen, BLACK, player_block["rect"])
        screen.blit(player_block["img"], (player_block["rect"].x, player_block["rect"].y, player_w, player_h)) # autito player
        screen.blit(traffic_car_block["img"], (traffic_car_block["rect"].x, traffic_car_block["rect"].y, player_w, player_h))

        #Mostrar powerup
        screen.blit(health_powerup_image, (power_up_healt["rect"].x, power_up_healt["rect"].y))


        # Dibujar el puntaje en la pantalla
        if high_score != 0:
            mostrar_texto(screen, (100, 120), f"High: {high_score}", fuente_2, WHITE, BLACK)
        mostrar_texto(screen, (100, 80), f'Score: {score}', fuente_2, CYAN, BLACK)
        mostrar_texto(screen, (680 , 80), f'Healt % {health}', fuente_2, RED, BLACK)
                            
        pygame.display.flip() # actualiza la pantalla
        #       ----> FIN dibujar elementos en pantalla <----

    # Pantalla GAME OVER
    motor_carFX.stop()
    game_over_sound.play()
    mostrar_texto(screen, (CENTER_X, 300), "GAME OVER", fuente, RED, BLACK)
    mostrar_texto(screen, (CENTER_X, 500), "SPACE to retry", fuente_2, RED, BLACK)
    pygame.display.flip()
    wait_user(pygame.K_SPACE)

    if score > high_score:
        high_score = score

terminar()