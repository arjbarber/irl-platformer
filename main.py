import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.8
SCROLL_SPEED = 2

class Player:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, jump_power: int):
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.jump_power = jump_power * -1  # Invert jump power for upward movement
        self.velocity_y = 0
        self.is_jumping = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def check_collision(self, platforms: list):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
                elif self.velocity_y < 0:  # Moving up
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def prevent_falling_through_floor(self):
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)

def generate_platforms(platforms, player):
    # Remove platforms that are off-screen
    platforms = [platform for platform in platforms if platform.rect.top < HEIGHT]

    # Generate new platforms
    while len(platforms) < 5:  # Maintain at least 5 platforms
        last_platform = platforms[-1] if platforms else None
        new_x = random.randint(0, WIDTH - 200)
        new_y = last_platform.rect.top - random.randint(100, 150) if last_platform else HEIGHT - 100

        # Ensure the new platform is reachable
        if last_platform:
            max_horizontal_distance = player.speed * 10  # Adjust based on player's speed
            max_vertical_distance = abs(player.jump_power) * 2  # Adjust based on player's jump power
            attempts = 0
            max_attempts = 100  # Limit the number of attempts to prevent infinite loop
            while (abs(new_x - last_platform.rect.x) > max_horizontal_distance or abs(new_y - last_platform.rect.top) > max_vertical_distance) and attempts < max_attempts:
                new_x = random.randint(0, WIDTH - 200)
                new_y = last_platform.rect.top - random.randint(100, 150)
                attempts += 1

        platforms.append(Platform(new_x, new_y, 200, 20))

    return platforms

def show_you_lost_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("You Lost!", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    pygame.display.set_caption("Scrolling Platformer")
    player = Player(WIDTH // 2, HEIGHT - 60, 50, 50, 5, 15)
    platforms = [
        Platform(200, 500, 400, 20),
        Platform(100, 400, 200, 20),
        Platform(500, 300, 200, 20),
    ]
    score = 0
    last_platform_y = player.rect.bottom

    run = True
    while run:
        clock.tick(FPS)
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        player.apply_gravity()
        player.check_collision(platforms)
        player.prevent_falling_through_floor()

        # Check if player touches the bottom of the screen
        if player.rect.bottom >= HEIGHT and score > 0:
            show_you_lost_screen()
            return main()  # Restart the game

        # Update score when a new platform is reached
        for platform in platforms:
            if player.rect.bottom <= platform.rect.top and platform.rect.top < last_platform_y:
                score += 1
                last_platform_y = platform.rect.top

        # Scroll platforms down if the player is above a certain height
        if player.rect.top < HEIGHT // 3:
            scroll_amount = HEIGHT // 3 - player.rect.top
            player.rect.y += scroll_amount
            for platform in platforms:
                platform.rect.y += scroll_amount

        # Generate new platforms
        platforms = generate_platforms(platforms, player)

        # Draw platforms and player
        for platform in platforms:
            platform.draw(screen)
        player.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()