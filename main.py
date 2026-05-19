import pygame
import constants as const

from environment import Environment
from entities.game_object import Game_object
from entities.bullet import Bullet

class TestBlock(Game_object):
    # Dodajemy parametr shootBullet w konstruktorze
    def __init__(self, shootBullet, x: float = 0.0, y: float = 0.0, width: float = 50.0, height: float = 50.0, color: tuple = const.BLUE):
        super().__init__(x, y, width, height, color)
        self.speed = 3
        
        # 1. NAPRAWA: Domyślny kierunek, żeby można było strzelać bez wcześniejszego ruchu
        self.vector = (0, -1) 
        self.shoot_cooldown = 0
        
        # Zapisujemy referencję do funkcji dodającej obiekty do środowiska
        self.shootBullet = shootBullet

    def update(self):
        keys = pygame.key.get_pressed()
        
        # 2. NAPRAWA: Zmieniamy na elif, aby zablokować ruch po skosie i chronić poprawność wektora
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.hitbox.y -= self.speed
            self.vector = (0, -1)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.hitbox.y += self.speed
            self.vector = (0, 1)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.hitbox.x -= self.speed
            self.vector = (-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.hitbox.x += self.speed
            self.vector = (1, 0)

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot_cooldown = const.FPS * 0.5
            bullet = Bullet(self.hitbox.centerx, self.hitbox.centery, const.BULLET_SPEED, self.vector)
            
            self.shootBullet(bullet)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

def main():
    game = Environment()
    
    test_block = TestBlock(shootBullet=game.game_objects.append, x=100, y=100, width=50, height=50, color=(0, 255, 0))
    game.game_objects.append(test_block)

    game.run()

if __name__ == "__main__":
    main()