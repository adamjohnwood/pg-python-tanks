import random

# Local imports
from entities.game_object import Game_object
import constants as CONST

class PowerUp(Game_object):
    def __init__(self, x: int, y: int):
        self.type = random.choice(list(CONST.POWERUP_TYPES.keys()))
        powerup_data = CONST.POWERUP_TYPES[self.type]
        super().__init__(x, y, CONST.POWERUP_SIZE, CONST.POWERUP_SIZE, powerup_data['color'])
        self.lifetime = CONST.POWERUP_LIFETIME
    
    def update(self):
        self.lifetime -= 1
