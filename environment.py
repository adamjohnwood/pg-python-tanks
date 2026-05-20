import pygame

#local imports
import constants as CONST
from entities.bullet import Bullet
from entities.tank import Tank
from entities.player_tank import Player_tank

class Environment:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CONST.WINDOW_WIDTH, CONST.WINDOW_HEIGHT))
        pygame.display.set_caption("PG-PYTHON-TANKS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_objects = []

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.check_collisions()
            self.draw()
            self.clock.tick(CONST.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_collisions(self):
        bullets = [obj for obj in self.game_objects if isinstance(obj, Bullet)]
        
        for bullet_1st in bullets:
            if bullet_1st not in self.game_objects:
                continue
            for bullet_2nd in bullets:
                if bullet_1st != bullet_2nd and bullet_2nd in self.game_objects:
                    if bullet_1st.hitbox.colliderect(bullet_2nd.hitbox):
                        self.game_objects.remove(bullet_1st)
                        self.game_objects.remove(bullet_2nd)
                        break






        bullets = [obj for obj in self.game_objects if isinstance(obj, Bullet)]
        tanks = [obj for obj in self.game_objects if isinstance(obj, Tank)]
        for bullet in bullets:
            for tank in tanks:
                if bullet.hitbox.colliderect(tank.hitbox):
                    if (bullet.owner == 'player' and not isinstance(tank, Player_tank)) or (bullet.owner == 'enemy' and isinstance(tank, Player_tank)):
                        tank.health -= bullet.damage
                        if bullet in self.game_objects:
                            self.game_objects.remove(bullet)
                        
                        if tank.health <= 0:
                            if tank in self.game_objects:
                                self.game_objects.remove(tank)
                                if isinstance(tank, Player_tank):
                                    print("Player tank destroyed! GAME OVER!")
                                    self.running = False
                        break

    def update(self):
        for obj in self.game_objects[:]:
            obj.update()
            if isinstance(obj, Bullet):
                if (obj.hitbox.x < 0 or obj.hitbox.x > CONST.WINDOW_WIDTH or
                    obj.hitbox.y < 0 or obj.hitbox.y > CONST.WINDOW_HEIGHT):
                    self.game_objects.remove(obj)

    def draw(self):
        self.screen.fill(CONST.BLACK)
        for obj in self.game_objects:
            obj.draw(self.screen)
            
        pygame.display.flip()

if __name__ == "__main__":
    env = Environment()
    env.run()