import pygame

# Local imports
import constants as CONST
from entities.tank import Tank
from entities.bullet import Bullet

class Player_tank(Tank):
    def __init__(self, x: int = 0, y: int = 0, tank_type: str = 'BasicTank', fire_action=None):
        super().__init__(x, y, tank_type)
        
        self.image.fill(CONST.GREEN)

        self.fire_action = fire_action

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movement and direction
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.hitbox.y -= self.speed
            self.vector = CONST.UP
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.hitbox.y += self.speed
            self.vector = CONST.DOWN
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.hitbox.x -= self.speed
            self.vector = CONST.LEFT
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.hitbox.x += self.speed
            self.vector = CONST.RIGHT

        # Shooting
        if keys[pygame.K_SPACE] and self.shoot_cooldown_timer <= 0:
            self.shoot_cooldown_timer = self.shoot_cooldown
            bullet = Bullet(self.hitbox.centerx, self.hitbox.centery, self.damage, CONST.BULLET_SPEED, self.vector, owner='player')
            if self.fire_action:
                self.fire_action(bullet)

        if self.shoot_cooldown_timer > 0:
            self.shoot_cooldown_timer -= 1
