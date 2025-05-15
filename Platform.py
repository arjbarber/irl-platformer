import pygame
import config
pygame.init()

class Platform:
    def __init__(self, x, y, width, height, platform_number):
        self.platform_number: int = platform_number
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, config.BLACK, self.rect)