# Constants for the game
GAME_TITLE = "PG Python Tanks"
GAME_WIDTH = 840
GAME_HEIGHT = 600
HUD_WIDTH = 200
WINDOW_WIDTH = GAME_WIDTH + HUD_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT
FPS = 60

# Map is 21x15 tiles, each tile is 40x40 pixels

# Sizes and speeds
OBJECT_SIZE = 40
TANK_SIZE = 40
BULLET_SIZE = 5
BULLET_SPEED = 10

BASE_HEALTH = 10
BRICK_HEALTH = 150

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BASE_COLOR = WHITE
BRICK_COLOR = (139, 69, 19)
STEEL_COLOR = (128, 128, 128)
WATER_COLOR = (0, 119, 190)
BUSH_COLOR = (34, 139, 34)
ICE_COLOR = (173, 216, 230)

# Tank types:
TANK_TYPES = {
    "BasicTank":   {"speed": 2, "health": 100, "damage": 50,  "cooldown": int(1.5 * FPS),  "color": RED},
    "FastTank":    {"speed": 4, "health": 50,  "damage": 20,  "cooldown": int(0.8 * FPS),  "color": YELLOW},
    "ArmoredTank": {"speed": 1, "health": 250, "damage": 50,  "cooldown": int(2.0 * FPS),  "color": STEEL_COLOR},
    "ShooterTank": {"speed": 1, "health": 50, "damage": 100, "cooldown": int(2.5 * FPS), "color": BLUE},
}
