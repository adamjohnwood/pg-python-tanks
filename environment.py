import pygame
import random

#local imports
import constants as CONST
from entities.bullet import Bullet
from entities.tank import Tank
from entities.player_tank import Player_tank
from entities.enemy_tank import Enemy_tank
from map.levels import ALL_LEVELS
from map.tiles import Base, BrickWall, SteelWall, Water, Bush, Ice

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
        self.running = True
        self.game_objects = []

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

    def check_collisions(self):
        bullets = [obj for obj in self.game_objects if isinstance(obj, Bullet)]
        tanks = [obj for obj in self.game_objects if isinstance(obj, Tank)]
        impassable_tiles = [obj for obj in self.game_objects if isinstance(obj, (BrickWall, SteelWall, Water, Base))]
        solid_tiles = [obj for obj in self.game_objects if isinstance(obj, (BrickWall, SteelWall, Base))]

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

            # With other tanks
            for other_tank in tanks:
                if tank != other_tank and tank.hitbox.colliderect(other_tank.hitbox):
                    tank.hitbox.x -= tank.vector[0] * tank.speed
                    tank.hitbox.y -= tank.vector[1] * tank.speed
                    isCollision = True
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
                        tank.health -= bullet.damage
                        if bullet in self.game_objects:
                            self.game_objects.remove(bullet)
                        
                        if tank.health <= 0 and tank in self.game_objects:
                            self.game_objects.remove(tank)
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
        for obj in self.game_objects[:]:
            obj.update()
        self.spawn_enemy()

    def draw(self):
        self.screen.fill(CONST.BLACK)
        for obj in self.game_objects:
            obj.draw(self.screen)
        self.draw_text()  
        pygame.display.flip()

    def draw_text(self):
        hud_background = pygame.Rect(CONST.GAME_WIDTH, 0, CONST.HUD_WIDTH, CONST.WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, CONST.STEEL_COLOR, hud_background)

        pygame.draw.line(self.screen, CONST.WHITE, (CONST.GAME_WIDTH, 0), (CONST.GAME_WIDTH, CONST.WINDOW_HEIGHT), 3)

        enemies_count = len([obj for obj in self.game_objects if isinstance(obj, Enemy_tank)])
        enemies_count += len(self.enemies_pool)
        player = next((obj for obj in self.game_objects if isinstance(obj, Player_tank)), None)

        x_margin = CONST.GAME_WIDTH + 10

        level_number_text = self.font.render(f'Level: {self.current_level}', True, CONST.BLACK)
        enemies_count_text = self.font.render(f'Enemies: {enemies_count}', True, CONST.RED)

        self.screen.blit(level_number_text, (x_margin, 30))
        self.screen.blit(enemies_count_text, (x_margin, 70))

        health_bar_label = self.font.render('Health:', True, CONST.WHITE)
        self.screen.blit(health_bar_label, (x_margin, 150))
    
        if player:
            healthbar_width = CONST.HUD_WIDTH - 20
            
            hp_ratio = max(player.health, 0) / 100
            healthbar_fill_width = int(healthbar_width * hp_ratio)

            pygame.draw.rect(self.screen, CONST.WHITE, (x_margin, 180, healthbar_width, 30))
            pygame.draw.rect(self.screen, CONST.GREEN, (x_margin, 180, healthbar_fill_width, 30))
            pygame.draw.rect(self.screen, CONST.BLACK, (x_margin, 180, healthbar_width, 30), 3)

            hp_text = self.font.render(f'{max(player.health, 0)} HP', True, CONST.BLACK)
            self.screen.blit(hp_text, (x_margin + 5, 185))
        else:
            health_text = self.font.render('GAME OVER!', True, CONST.WHITE)
            self.screen.blit(health_text, (x_margin, 180))

if __name__ == "__main__":
    env = Environment()
    env.run()