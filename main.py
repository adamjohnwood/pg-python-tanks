import pygame
import random

# Local imports
import constants as CONST
from environment import Environment
from entities.player_tank import Player_tank
from entities.enemy_tank import Enemy_tank

def main():
    game = Environment()
    game.run()

if __name__ == "__main__":
    main()