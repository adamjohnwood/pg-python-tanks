import random

# Local imports
import constants as CONST

# --- START OF CODE WRITTEN BY AI --- 
# I thought it would be funny to do that, I told chatGPT to make simple weight based movement system

class BaseAI:
    def get_new_direction(self, assault_dir):
        directions = [CONST.DOWN, CONST.UP, CONST.RIGHT, CONST.LEFT]
        return random.choice(directions)
        
    def should_shoot(self):
        return random.random() < 0.02 

class AssaultAI(BaseAI):
    def get_new_direction(self, assault_dir):
        perp1 = (-assault_dir[1], assault_dir[0])
        perp2 = (assault_dir[1], -assault_dir[0])
        reverse = (-assault_dir[0], -assault_dir[1])
        
        choices = [
            assault_dir, assault_dir, assault_dir, assault_dir, assault_dir,
            perp1, perp1,
            perp2, perp2,
            reverse
        ]
        return random.choice(choices)
        
    def should_shoot(self):
        return random.random() < 0.03

class DefenderAI(BaseAI):
    def get_new_direction(self, assault_dir):
        perp1 = (-assault_dir[1], assault_dir[0])
        perp2 = (assault_dir[1], -assault_dir[0])
        reverse = (-assault_dir[0], -assault_dir[1])
        
        choices = [
            perp1, perp1, perp1, perp1,
            perp2, perp2, perp2, perp2,
            assault_dir, reverse
        ]
        return random.choice(choices)

class SniperAI(BaseAI):
    def should_shoot(self):
        return random.random() < 0.01

# --- END ---

AI_PROFILES = {
    "BasicTank": BaseAI(),
    "FastTank": AssaultAI(),       
    "ArmoredTank": DefenderAI(),   
    "ShooterTank": SniperAI()
}