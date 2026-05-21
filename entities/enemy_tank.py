import random

# Local imports
import constants as CONST
from entities.tank import Tank
from entities.bullet import Bullet

class Enemy_tank(Tank):
    def __init__(self, x: int = 0, y: int = 0, tank_type: str = 'BasicTank', fire_action=None):
        super().__init__(x, y, tank_type)
        self.image.fill(CONST.RED)
        self.fire_action = fire_action

        self.move_timer = random.randint(CONST.FPS, CONST.FPS * 3)
        self.vector = random.choice([CONST.UP, CONST.DOWN, CONST.LEFT, CONST.RIGHT])

    def change_direction(self):
        possible_directions = [CONST.UP, CONST.DOWN, CONST.LEFT, CONST.RIGHT]
        if self.vector in possible_directions:
            possible_directions.remove(self.vector)
        self.vector = random.choice(possible_directions)
        self.move_timer = random.randint(CONST.FPS, CONST.FPS * 3)

    def update(self):
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.change_direction()

        self.hitbox.x += self.vector[0] * self.speed
        self.hitbox.y += self.vector[1] * self.speed

        if self.shoot_cooldown_timer <= 0 and self.fire_action:
            bullet = Bullet(self.hitbox.centerx, self.hitbox.centery, self.damage, CONST.BULLET_SPEED, self.vector, owner='enemy')
            self.fire_action(bullet)
            self.shoot_cooldown_timer = self.shoot_cooldown

        if self.shoot_cooldown_timer > 0:
            self.shoot_cooldown_timer -= 1