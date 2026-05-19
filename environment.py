import pygame   
import sys

class Environment:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((255, 255, 255))  # Clear the screen with white
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second
