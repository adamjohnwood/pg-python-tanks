import constants as const
from entities.game_object import Game_object

class Bullet(Game_object):
    def __init__(self, x, y, speed, vector):
        super().__init__(x, y, 5, 5, const.YELLOW)
        self.speed = speed
        self.vector = vector

    def update(self):
        self.hitbox.x += self.vector[0] * self.speed
        self.hitbox.y += self.vector[1] * self.speed
