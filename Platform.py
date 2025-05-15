import pygame
import config
import os
pygame.init()

PLATFORM = pygame.image.load(os.path.join('assets', 'platform.png'))

class Platform:
    def __init__(self, x, y, width, height, platform_number):
        self.platform_number: int = platform_number
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.surface: pygame.Surface = pygame.transform.scale(PLATFORM, (self.rect.width, self.rect.height))

    def draw(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))