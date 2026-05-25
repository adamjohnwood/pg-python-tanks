import pygame

# Local imports
import constants as CONST
from entities.game_object import Game_object
from assets.assets import IMAGES


class Tank(Game_object):
    def __init__(self, x: int = 0, y: int = 0, tank_type: str = 'BasicTank'):
        tank_data = CONST.TANK_TYPES.get(tank_type, CONST.TANK_TYPES['BasicTank'])
        
        if tank_type == 'player':
            self.original_image = IMAGES['player']
        else:
            self.original_image = IMAGES.get(tank_type, IMAGES['BasicTank'])
        
        super().__init__(x, y, CONST.TANK_SIZE, CONST.TANK_SIZE, tank_data["color"], image=self.original_image)

        self.speed = tank_data["speed"]
        self.health = tank_data["health"]
        self.shield_timer = 0
        self.damage = tank_data["damage"]
        self.shoot_cooldown = tank_data["cooldown"]
        self.shoot_cooldown_timer = 0
        self.vector = CONST.UP

    def update(self):
        pass

    def update_rotation(self):
        if self.vector == CONST.UP:
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.vector == CONST.LEFT:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.vector == CONST.DOWN:
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.vector == CONST.RIGHT:
            self.image = pygame.transform.rotate(self.original_image, -90)

    def draw(self, screen):
        self.update_rotation()
        super().draw(screen)