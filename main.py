import pygame
import sys
import random
from Platform import Platform
from Player import Player
import config
pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

clock = pygame.time.Clock()

def generate_platforms(platforms, player):
    # Remove platforms that are off-screen
    platforms = [platform for platform in platforms if platform.rect.top < config.HEIGHT]

    # Generate new platforms
    while len(platforms) < 5:  # Maintain at least 5 platforms
        last_platform = platforms[-1] if platforms else None
        new_x = random.randint(0, config.WIDTH - 200)
        new_y = last_platform.rect.top - random.randint(100, 150) if last_platform else config.HEIGHT - 100

        # Ensure the new platform is reachable
        if last_platform:
            max_horizontal_distance = player.speed * 10  # Adjust based on player's speed
            max_vertical_distance = abs(player.jump_power) * 2  # Adjust based on player's jump power
            attempts = 0
            max_attempts = 100  # Limit the number of attempts to prevent infinite loop
            while (abs(new_x - last_platform.rect.x) > max_horizontal_distance or abs(new_y - last_platform.rect.top) > max_vertical_distance) and attempts < max_attempts:
                new_x = random.randint(0, config.WIDTH - 200)
                new_y = last_platform.rect.top - random.randint(100, 150)
                attempts += 1

        # Assign a unique platform number and determine platform type
        platform_number = platforms[-1].platform_number + 1 if platforms else 0
        platform_type = "red" if random.randint(1, 10) == 1 else "green" if random.randint(1, 10) == 1 else "normal"
        platforms.append(Platform(new_x, new_y, 200, 20, platform_number, platform_type))

    return platforms

def show_you_lost_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("You Lost!", True, config.BLACK)
    screen.fill(config.WHITE)
    screen.blit(text, (config.WIDTH // 2 - text.get_width() // 2, config.HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    pygame.display.set_caption("Scrolling Platformer")
    player = Player(config.WIDTH // 2, 500, 50, 50, 10, 15)
    platforms = [
        Platform(200, 500, 400, 20, 0),
        Platform(100, 400, 200, 20, 1),
        Platform(500, 300, 200, 20, 2),
    ]

    run = True
    score = 0
    while run:
        clock.tick(config.FPS)
        screen.fill(config.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        player.apply_gravity()
        score = player.check_collision(platforms, score)
        player.prevent_falling_through_floor()
        player.move(keys)
        print(player.velocity_y)

        # Handle green platform effect
        for platform in platforms:
            if platform.type == "green" and player.rect.colliderect(platform.rect):
                player.jump_power = 30  # Double jump power
                break
        else:
            player.jump_power = 15  # Reset jump power

        # Check if player touches the bottom of the screen
        if player.rect.bottom >= config.HEIGHT and score > 0:
            show_you_lost_screen()
            return main()  # Restart the game

        # Scroll platforms down if the player is above a certain height
        if player.rect.top < config.HEIGHT // 3:
            scroll_amount = config.HEIGHT // 3 - player.rect.top
            player.rect.y += scroll_amount
            for platform in platforms:
                platform.rect.y += scroll_amount

        # Generate new platforms
        platforms = generate_platforms(platforms, player)

        # Update and draw platforms
        for platform in platforms:
            platform.update(player)  # Pass the player to the update method
            platform.draw(screen)

        # Draw the player
        player.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score-1}", True, config.BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
