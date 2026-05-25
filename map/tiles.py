# Local imports
import constants as CONST
from entities.game_object import Game_object
from assets.assets import IMAGES

class Tile(Game_object):
    def __init__(self, x: int, y: int, symbol: str, color: tuple = CONST.BRICK_COLOR):
        super().__init__(x, y, CONST.OBJECT_SIZE, CONST.OBJECT_SIZE, color, image=IMAGES[symbol])
        
        self.destructible = False
        self.health = 1000

    def update(self):
        pass

class Base(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 'B', CONST.BASE_COLOR)
        self.destructible = True
        self.health = CONST.BASE_HEALTH

class BrickWall(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '#', CONST.BRICK_COLOR)
        self.destructible = True
        self.health = CONST.BRICK_HEALTH

class SteelWall(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '@', CONST.STEEL_COLOR)

class Water(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '~', CONST.WATER_COLOR)

class Bush(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '*', CONST.BUSH_COLOR)

class Ice(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, '-', CONST.ICE_COLOR)