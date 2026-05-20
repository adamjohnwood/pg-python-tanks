import constants as CONST
from entities.game_object import Game_object

class Bullet(Game_object):
    def __init__(self, x, y, damage, speed, vector, owner=None):
        super().__init__(x, y, CONST.BULLET_SIZE, CONST.BULLET_SIZE, CONST.YELLOW)
        self.damage = damage
        self.speed = speed
        self.vector = vector
        self.owner = owner

    def update(self):
        self.hitbox.x += self.vector[0] * self.speed
        self.hitbox.y += self.vector[1] * self.speed
