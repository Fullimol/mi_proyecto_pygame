WIDTH = 800
HEIGHT = 600
SIZE_SCREEN = (WIDTH, HEIGHT)
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
CENTER_SCREEN = (CENTER_X, CENTER_Y)
FPS = 65
SPEED = 5

# Colors:
RED = (255, 0, 0)
GREEN = (0, 120, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
BROWN = (93, 40, 1)

# Player:
player_w = 68
player_h = 115
player_center_X = CENTER_X - player_w // 2
player_center_Y = CENTER_Y - player_h // 2

# Road:
scroll_speed = 16

road_w = 350
road_h = HEIGHT
road_top = 0
road_left = CENTER_X - road_w // 2 
road_right = road_left + road_w

tierra_w = 500
tierra_h = HEIGHT
tierra_top = 0
tierra_left = 148

pasto_w = WIDTH
pasto_h = HEIGHT
pasto_top = 0
pasto_left = 0

# Traffic:
traffic_car_w = 68
traffic_car_h = 115
reduce_speed = 8
traffic_speed = 10
aparecer_arriba = -90

# PowerUp:
powerup_w = 40
powerup_h = 40
healt_move_speed_x = 6

# Hole:
danger_hole_w = 100
danger_hole_h = 100