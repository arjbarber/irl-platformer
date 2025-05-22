import pygame
pygame.init()
import config
import cv2
import mediapipe as mp
import os

GRAVITY = 0.8

PLAYER = pygame.image.load(os.path.join('assets', 'player.png'))

class Player:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, jump_power: int):
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.speed: int = speed
        self.jump_power: int = jump_power * -1  # Invert jump power for upward movement
        self.velocity_y: int = 0
        self.is_jumping: bool = False
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.cap = cv2.VideoCapture(0)
        self.height = []
        self.surface: pygame.Surface = pygame.transform.scale(PLAYER, (self.rect.width, self.rect.height))

    def move(self, keys):
        # # Use arrow keys for movement
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed
        if keys[pygame.K_UP] and not self.is_jumping:
            self.jump()

        # Use camera input for movement
        ret, frame = self.cap.read()
        if not ret:
            return  # Skip if no frame is captured

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Use landmarks for movement (e.g., nose for horizontal movement)
            nose_x = 1 - landmarks[self.mp_pose.PoseLandmark.NOSE].x  # Reverse direction

            # Map nose_x (0 to 1) to screen width
            screen_width = config.WIDTH
            player_x = int(nose_x * screen_width)

            # Update player position based on nose position
            self.rect.x = player_x - self.rect.width // 2 if player_x - self.rect.width // 2 > 0 else 0
            self.rect.x = player_x + self.rect.width // 2 if player_x + self.rect.width // 2 < screen_width else screen_width - self.rect.width

            # Jumping logic
            self.height.append(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y)
            if len(self.height) > 5:
                self.height.pop(0)

            # Check if the hip has moved upward significantly to trigger a jump
            if len(self.height) > 2 and (self.height[-2] - self.height[-1] > 0.05) and not self.is_jumping:
                self.jump()

            # Draw landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS
            )

        # Display the camera feed
        frame = cv2.flip(frame, 1)  # Mirror the frame in the x direction
        cv2.imshow("Camera Feed", frame)
        cv2.waitKey(1)

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def check_collision(self, platforms: list, score: int = 0):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
                    return platform.platform_number + 1  # Increment score based on platform number
        return score

    def prevent_falling_through_floor(self):
        if self.rect.bottom > config.HEIGHT:
            self.rect.bottom = config.HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        self.velocity_y = self.jump_power
        self.is_jumping = True

    def draw(self, surface):
        pygame.draw.rect(surface, config.BLUE, self.rect)