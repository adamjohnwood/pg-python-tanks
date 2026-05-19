import pygame
from abc import ABC, abstractmethod

class Game_object(ABC):
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 50.0, height: float = 50.0, color: tuple = (255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    @abstractmethod
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.hitbox.x, self.hitbox.y))