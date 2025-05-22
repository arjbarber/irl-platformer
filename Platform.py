import pygame
import config
import os
pygame.init()

PLATFORM = pygame.image.load(os.path.join('assets', 'platform.png'))
RED_PLATFORM = pygame.image.load(os.path.join('assets', 'red_platform.png'))
GREEN_PLATFORM = pygame.image.load(os.path.join('assets', 'green_platform.png'))

class Platform:
    def __init__(self, x, y, width, height, platform_number, platform_type="normal"):
        self.platform_number: int = platform_number
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.type: str = platform_type
        self.surface: pygame.Surface = pygame.transform.scale(
            RED_PLATFORM if self.type == "red" else GREEN_PLATFORM if self.type == "green" else PLATFORM,
            (self.rect.width, self.rect.height)
        )
        self.break_timer = 3 * config.FPS if self.type == "red" else None  # 3 seconds for red platforms

    def update(self):
        if self.type == "red" and self.break_timer is not None:
            self.break_timer -= 1
            if self.break_timer <= 0:
                self.rect.y = config.HEIGHT + 1  # Move off-screen to "break"

    def draw(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))