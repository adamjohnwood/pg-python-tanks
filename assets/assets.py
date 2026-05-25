import pygame

IMAGES = {}
# --- START OF CODE WRITTEN BY AI --- 
def load_assets():
    
    # Tiles
    IMAGES['#'] = pygame.image.load('assets/brick.png').convert_alpha()
    IMAGES['@'] = pygame.image.load('assets/steel.png').convert_alpha()
    IMAGES['~'] = pygame.image.load('assets/water.png').convert_alpha()
    IMAGES['*'] = pygame.image.load('assets/bush.png').convert_alpha()
    IMAGES['-'] = pygame.image.load('assets/ice.png').convert_alpha()
    IMAGES['B'] = pygame.image.load('assets/base.png').convert_alpha()
    
    # Tanks
    IMAGES['player'] = pygame.image.load('assets/player.png').convert_alpha()
    IMAGES['BasicTank'] = pygame.image.load('assets/enemy_basic.png').convert_alpha()
    IMAGES['FastTank'] = pygame.image.load('assets/enemy_fast.png').convert_alpha()
    IMAGES['ArmoredTank'] = pygame.image.load('assets/enemy_armored.png').convert_alpha()
    IMAGES['ShooterTank'] = pygame.image.load('assets/enemy_shooter.png').convert_alpha()

# --- END ---