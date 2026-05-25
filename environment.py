import pygame
import random

#local imports
import constants as CONST
from entities.bullet import Bullet
from entities.tank import Tank
from entities.player_tank import Player_tank
from entities.enemy_tank import Enemy_tank
from entities.powerups import PowerUp
from map.levels import ALL_LEVELS
from map.tiles import Base, BrickWall, SteelWall, Water, Bush, Ice
from assets.assets import load_assets, IMAGES

TILES_CLASSES = {
    '#': BrickWall,
    '@': SteelWall,
    '~': Water,
    '*': Bush,
    '-': Ice,
    'B': Base
}

class Environment:
    def __init__(self):
        # Game initialization
        pygame.init()
        self.screen = pygame.display.set_mode((CONST.WINDOW_WIDTH, CONST.GAME_HEIGHT))
        pygame.display.set_caption("PG-PYTHON-TANKS")
        self.clock = pygame.time.Clock()
        load_assets()
        self.running = True
        self.game_objects = []
        self.state = 'PLAYING'

        self.current_level = 1
        self.spawn_timer = 0
        self.max_enemies_on_map = 0

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

        self.load_level()

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
            # Toggle pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'PAUSED' if self.state == 'PLAYING' else 'PLAYING'

    def check_collisions(self):
        bullets = [obj for obj in self.game_objects if isinstance(obj, Bullet)]
        tanks = [obj for obj in self.game_objects if isinstance(obj, Tank)]
        impassable_tiles = [obj for obj in self.game_objects if isinstance(obj, (BrickWall, SteelWall, Water, Base))]
        solid_tiles = [obj for obj in self.game_objects if isinstance(obj, (BrickWall, SteelWall, Base))]
        ice_tiles = [obj for obj in self.game_objects if isinstance(obj, Ice)]
        powerups = [obj for obj in self.game_objects if isinstance(obj, PowerUp)]

        # Check tanks collisions
        for tank in tanks:
            isCollision = False

            # With map borders
            if tank.hitbox.left < 0:
                tank.hitbox.left = 0
                isCollision = True
            if tank.hitbox.right > CONST.GAME_WIDTH:
                tank.hitbox.right = CONST.GAME_WIDTH
                isCollision = True
            if tank.hitbox.top < 0:
                tank.hitbox.top = 0
                isCollision = True
            if tank.hitbox.bottom > CONST.GAME_HEIGHT:
                tank.hitbox.bottom = CONST.GAME_HEIGHT
                isCollision = True

            # With impassable tiles
            for tile in impassable_tiles:
                if tank.hitbox.colliderect(tile.hitbox):
                    tank.hitbox.x -= tank.vector[0] * tank.speed
                    tank.hitbox.y -= tank.vector[1] * tank.speed
                    isCollision = True
                    break

            # With ice
            tank.on_ice = False
            for ice in ice_tiles:
                if ice.hitbox.collidepoint(tank.hitbox.center):
                    tank.on_ice = True
                    break
                
            # With other tanks
            for other_tank in tanks:
                if tank != other_tank and tank.hitbox.colliderect(other_tank.hitbox):
                    tank.hitbox.x -= tank.vector[0] * tank.speed
                    tank.hitbox.y -= tank.vector[1] * tank.speed
                    isCollision = True
                    break

            # With powerups
            for powerup in powerups:
                if powerup in self.game_objects and tank.hitbox.colliderect(powerup.hitbox):
                    if isinstance(tank, Player_tank):
                        bonus_value = CONST.POWERUP_TYPES[powerup.type]['value']
                        if powerup.type == 'heal':
                            tank.health = min(tank.health + bonus_value, 100)
                        elif powerup.type == 'shield':
                            tank.shield_timer = bonus_value
                        elif powerup.type == 'bomb':
                            enemies_to_destroy = [enemy for enemy in tanks if isinstance(enemy, Enemy_tank)]
                            for enemy in enemies_to_destroy:
                                if enemy in self.game_objects:
                                    self.game_objects.remove(enemy)

                    self.game_objects.remove(powerup)
                    break

            # Make enemey tanks change direction on collision
            if isCollision and isinstance(tank, Enemy_tank):
                tank.change_direction()

        # Check bullets collisions
        for bullet in bullets:
            if bullet not in self.game_objects:
                continue
            
            # With map borders
            if(bullet.hitbox.left < 0 or bullet.hitbox.right > CONST.GAME_WIDTH or bullet.hitbox.top < 0 or bullet.hitbox.bottom > CONST.GAME_HEIGHT):
                self.game_objects.remove(bullet)
                continue

            if bullet not in self.game_objects:
                continue

            # With tanks
            for tank in tanks:
                if bullet.hitbox.colliderect(tank.hitbox):
                    if (bullet.owner == 'player' and not isinstance(tank, Player_tank)) or (bullet.owner == 'enemy' and isinstance(tank, Player_tank)):
                        if isinstance(tank, Player_tank) and tank.shield_timer > 0:
                            if bullet in self.game_objects:
                                self.game_objects.remove(bullet)
                                break    
                        tank.health -= bullet.damage
                        if bullet in self.game_objects:
                            self.game_objects.remove(bullet)
                        
                        if tank.health <= 0 and tank in self.game_objects:
                            self.game_objects.remove(tank)
                            if isinstance(tank, Enemy_tank):
                                if random.random() < 0.20:
                                    self.game_objects.append(PowerUp(tank.hitbox.x, tank.hitbox.y))
                            if isinstance(tank, Player_tank):
                                print("Player tank destroyed! GAME OVER!")
                                self.running = False
                        break
            
            if bullet not in self.game_objects:
                continue
            
            # With solid tiles
            for tile in solid_tiles:
                if bullet.hitbox.colliderect(tile.hitbox):
                    self.game_objects.remove(bullet)
                    
                    if hasattr(tile, 'destructible') and tile.destructible:
                        tile.health -= bullet.damage
                        if tile.health <= 0 and tile in self.game_objects:
                            self.game_objects.remove(tile)

                            if isinstance(tile, Base):
                                print("Base destroyed! GAME OVER!")
                                self.running = False
                    break

            if bullet not in self.game_objects:
                continue

            # With other bullets
            for other_bullet in bullets:
                if bullet != other_bullet and bullet in self.game_objects:
                    if bullet.hitbox.colliderect(other_bullet.hitbox):
                        self.game_objects.remove(bullet)
                        self.game_objects.remove(other_bullet)
                        break

    def load_level(self):
        # Clear existing game objects
        self.game_objects.clear()

        # Check if there are more levels to load
        if self.current_level > len(ALL_LEVELS):
            print("Congratulations! You've completed all levels!")
            self.running = False
            return

        level_data = ALL_LEVELS[self.current_level - 1]

        # Load new level
        level_map = level_data['map']
        for row_index, row in enumerate(level_map):
            for col_index, tile_char in enumerate(row):
                if tile_char in TILES_CLASSES:
                    tile_class = TILES_CLASSES[tile_char]
                    x = col_index * CONST.OBJECT_SIZE
                    y = row_index * CONST.OBJECT_SIZE
                    tile = tile_class(x, y) # I didn't know that I can do this, it's pretty cool that you can take name and use it as a variable
                    self.game_objects.append(tile)

        # Spawn player tank
        player_spawn = level_data['player_spawn']
        player = Player_tank(x=player_spawn[0] * CONST.OBJECT_SIZE, y=player_spawn[1] * CONST.OBJECT_SIZE, fire_action=self.game_objects.append)
        self.game_objects.append(player)

        # Get enemy spawn info
        self.enemy_spawns = level_data['enemy_spawns']
        self.enemies_pool = list(level_data['enemies'])
        self.max_enemies_on_map = len(level_data['enemy_spawns'])
        self.assault_dir = level_data['assault_direction']

    def spawn_enemy(self):
        # Check if we can spawn a new enemy
        enemies_on_map = len([obj for obj in self.game_objects if isinstance(obj, Enemy_tank)])
        enemies_to_spawn = len(self.enemies_pool)

        if enemies_to_spawn > 0 and enemies_on_map < self.max_enemies_on_map:
            if self.spawn_timer <= 0:
                spawn_point = random.choice(self.enemy_spawns)
                random_enemy_type = random.choice(self.enemies_pool)
                self.enemies_pool.remove(random_enemy_type)

                enemy = Enemy_tank(x=spawn_point[0] * CONST.OBJECT_SIZE, y=spawn_point[1] * CONST.OBJECT_SIZE, tank_type=random_enemy_type, fire_action=self.game_objects.append, assault_dir=self.assault_dir)
                self.game_objects.append(enemy)
                self.spawn_timer = CONST.FPS * 2 # Spawn rate is 1 tank per 2 seconds
            else:
                self.spawn_timer -= 1
        elif enemies_to_spawn == 0 and enemies_on_map == 0:
            self.current_level += 1
            self.load_level()

    def update(self):
        if self.state != 'PLAYING': return
        self.spawn_enemy()
        for obj in self.game_objects[:]:
            obj.update()
            if isinstance(obj, PowerUp) and obj.lifetime <= 0:
                self.game_objects.remove(obj)
        
    def draw(self):
        self.screen.fill(CONST.BLACK)
        for obj in self.game_objects:
            obj.draw(self.screen)
            if isinstance(obj, Player_tank) and obj.shield_timer > 0:
                pygame.draw.circle(
                    self.screen,
                    CONST.CYAN,
                    obj.hitbox.center,
                    int(CONST.TANK_SIZE / 2) + 5,
                    3
                )
        self.draw_text()  

        if self.state == 'PAUSED':
            overlay = pygame.Surface((CONST.GAME_WIDTH, CONST.GAME_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pause_txt = self.font.render('PAUSED - PRESS ESC', True, (255, 255, 255))
            self.screen.blit(pause_txt, (CONST.GAME_WIDTH//2 - 80, CONST.GAME_HEIGHT//2))
            
        pygame.display.flip()

        pygame.display.flip()

    def draw_text(self):
        hud_rect = pygame.Rect(CONST.GAME_WIDTH, 0, CONST.HUD_WIDTH, CONST.WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, (25, 25, 30), hud_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (CONST.GAME_WIDTH, 0), (CONST.GAME_WIDTH, CONST.WINDOW_HEIGHT), 4)

        x_margin = CONST.GAME_WIDTH + 20
        
        level_txt = self.font.render(f'MISSION: {self.current_level}', True, (200, 200, 200))
        self.screen.blit(level_txt, (x_margin, 30))

        enemies_count = len([obj for obj in self.game_objects if isinstance(obj, Enemy_tank)]) + len(self.enemies_pool)
        enemies_txt = self.font.render(f'ENEMIES: {enemies_count}', True, (255, 100, 100))
        self.screen.blit(enemies_txt, (x_margin, 70))

        player = next((obj for obj in self.game_objects if isinstance(obj, Player_tank)), None)
        hp_label = self.font.render('HP STATUS:', True, (200, 200, 200))
        self.screen.blit(hp_label, (x_margin, 140))

        if player:
            hp_box = pygame.Rect(x_margin, 170, CONST.HUD_WIDTH - 40, 25)
            pygame.draw.rect(self.screen, (200, 200, 200), hp_box, 2)
            fill_width = int((hp_box.width - 4) * max(player.health, 0) / 100)
            pygame.draw.rect(self.screen, (0, 255, 150), (x_margin + 2, 172, fill_width, 21))
        else:
            game_over_txt = self.font.render('SYSTEM FAILURE', True, (255, 50, 50))
            self.screen.blit(game_over_txt, (x_margin, 170))

if __name__ == "__main__":
    env = Environment()
    env.run()