import pygame
import constants as CONST
from abc import ABC, abstractmethod

class Game_object(ABC):
    def __init__(self, x: int = 0, y: int = 0, width: int = CONST.OBJECT_SIZE, height: int = CONST.OBJECT_SIZE, color: tuple = CONST.WHITE, image = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(color)

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    @abstractmethod
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.hitbox.x, self.hitbox.y))