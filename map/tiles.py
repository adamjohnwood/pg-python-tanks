# Local imports
import constants as CONST
from entities.game_object import Game_object

class Tile(Game_object):
    def __init__(self, x: int = 0, y: int = 0, color: tuple = CONST.BRICK_COLOR):
        super().__init__(x, y, CONST.OBJECT_SIZE, CONST.OBJECT_SIZE, color)

    def update(self):
        pass

class BrickWall(Tile):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, CONST.BRICK_COLOR)
        self.health = CONST.BRICK_HEALTH

class SteelWall(Tile):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, CONST.STEEL_COLOR)