# Local imports
import constants as CONST
from entities.game_object import Game_object


class Tank(Game_object):
    def __init__(self, x: int = 0, y: int = 0, tank_type: str = 'BasicTank'):
        tank_data = CONST.TANK_TYPES.get(tank_type, CONST.TANK_TYPES['BasicTank'])
        super().__init__(x, y, CONST.TANK_SIZE, CONST.TANK_SIZE, tank_data["color"])

        self.speed = tank_data["speed"]
        self.health = tank_data["health"]
        self.damage = tank_data["damage"]
        self.shoot_cooldown = tank_data["cooldown"]
        self.shoot_cooldown_timer = 0
        self.vector = CONST.UP

    def update(self):
        pass