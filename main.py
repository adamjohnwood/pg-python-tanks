import pygame
import random

# Local imports
import constants as CONST
from environment import Environment
from entities.player_tank import Player_tank
from entities.enemy_tank import Enemy_tank

def main():
    game = Environment()
    
    me = Player_tank(fire_action=game.game_objects.append)
    game.game_objects.append(me)

    for i in range(random.randint(1, 5)):
        tanktype = random.choice(list(CONST.TANK_TYPES.keys())) 
        enemy = Enemy_tank(x=random.randint(0, CONST.WINDOW_WIDTH - CONST.TANK_SIZE), y=random.randint(0, CONST.WINDOW_HEIGHT - CONST.TANK_SIZE), tank_type=tanktype, fire_action=game.game_objects.append)
        game.game_objects.append(enemy)
    game.run()

if __name__ == "__main__":
    main()