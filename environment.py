import pygame
import sys
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, FPS, BLACK, WHITE

class Environment:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PG-PYTHON-TANKS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_objects = []

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        for obj in self.game_objects:
            obj.update()

    def draw(self):
        self.screen.fill(BLACK)
        for obj in self.game_objects:
            obj.draw(self.screen)
            
        pygame.display.flip()

if __name__ == "__main__":
    env = Environment()
    env.run()