# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# colors for flappybird
SKYBLUE = (112, 197, 206)

# game settings
WIDTH = 450
HEIGHT = 600
FPS = 60
SHOW_FPS = True
TITLE = "FlappyBird"
BGCOLOR = DARKGREY

# player properties
PLAYER_GRAV = 0.5
PLAYER_JUMP = 11
PLAYER_FRICTION = 0.02
BOB_RANGE = 10
BOB_SPEED = 0.5
ROT_SPEED = 1

# ground properties
GROUND_HEIGHT = 75

# pipe properties
PIPE_WIDTH = 80
PIPE_SPRITE_HEIGHT = 500
PIPE_SPAWN_POSX = 500
PIPE_V_GAP = 150
PIPE_H_GAP = 200
PIPE_SPEED = 175 # pixels per second

# layers
PLAYER_LAYER = 3
GROUND_LAYER = 2
PIPE_LAYER = 1
