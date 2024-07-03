WIDTH = 800
HEIGHT = 600
SIZE_SCREEN = (WIDTH, HEIGHT)
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
CENTER_SCREEN = (CENTER_X, CENTER_Y)

FPS = 60
SPEED = 5

# Colors
RED = (255, 0, 0)
GREEN = (0, 120, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BROWN = (93, 40, 1)

# PLAYER:
player_w = 68
player_h = 95

# Road:
road_y = 0  # posicion inicial de la imagen de la calle
road_w = 350
road_h = HEIGHT
scroll_speed = 16
centrar_road = CENTER_X - road_w // 2
limte_x_road = centrar_road + road_w

tierra_w = 500
tierra_h = HEIGHT
tierra_x = 148
tierra_y = 0

pasto_w = WIDTH
pasto_h = HEIGHT
pasto_y = 0
pasto_x = 0


# Traffic:
traffic_car_w = 68
traffic_car_h = 95

van_car_w = 80
van_car_h = 100

reduce_speed = 8
traffic_speed = 10
aparecer_arriba = -80

# PowerUps:
powerup_w = 40
powerup_h = 40
healt_move_speed = 6

# Hole:
danger_hole_w = 100
danger_hole_h = 100