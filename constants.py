# Constants for the game
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 120

OBJECT_SIZE = 40
TANK_SIZE = 40
BULLET_SIZE = 5
BULLET_SPEED = 10

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

BRICK_COLOR = (139, 69, 19)
STEEL_COLOR = (128, 128, 128)
WATER_COLOR = (0, 119, 190)
BUSH_COLOR = (34, 139, 34)
ICE_COLOR = (173, 216, 230)

# Tank types:
TANK_TYPES = {
    "BasicTank":   {"speed": 3, "health": 100, "damage": 50,  "cooldown": int(0.5 * FPS),  "color": RED},
    "FastTank":    {"speed": 5, "health": 50,  "damage": 25,  "cooldown": int(0.3 * FPS),  "color": YELLOW},
    "ArmoredTank": {"speed": 2, "health": 200, "damage": 50,  "cooldown": int(0.8 * FPS),  "color": STEEL_COLOR},
    "ShooterTank": {"speed": 3, "health": 100, "damage": 100, "cooldown": int(0.25 * FPS), "color": BLUE},
}

BRICK_HEALTH = 150

