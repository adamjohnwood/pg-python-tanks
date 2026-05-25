import random

# Local imports
import constants as CONST
from entities.tank import Tank
from entities.bullet import Bullet
from ai.enemy_ai import AI_PROFILES

class Enemy_tank(Tank):
    def __init__(self, x: int, y: int, tank_type: str, fire_action, assault_dir):
        super().__init__(x, y, tank_type)
        self.fire_action = fire_action
        self.ai_brain = AI_PROFILES.get(tank_type, AI_PROFILES['BasicTank'])
        self.assault_dir = assault_dir
        self.move_timer = 0
        self.vector = random.choice([CONST.UP, CONST.DOWN, CONST.LEFT, CONST.RIGHT])

    def change_direction(self):
        self.vector = self.ai_brain.get_new_direction(self.assault_dir)
        self.move_timer = random.randint(CONST.FPS, CONST.FPS * 3)

    def update(self):
        self.move_timer -= 1

        if self.move_timer <= 0:
            self.change_direction()

        self.hitbox.x += self.vector[0] * self.speed
        self.hitbox.y += self.vector[1] * self.speed

        if self.ai_brain.should_shoot():
            bullet = Bullet(self.hitbox.centerx, self.hitbox.centery, self.damage, CONST.BULLET_SPEED, self.vector, owner='enemy')
            self.fire_action(bullet)