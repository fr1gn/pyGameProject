import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (147, 251, 253)

# Set up the screen
screen_width, screen_height = 1000, 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Air Hockey')

# Fonts
font = pygame.font.SysFont("comicsansms", 35)

# Game objects
goal_height = 150
goal_width = 20
goal1 = pygame.Rect(0, screen_height // 2 - goal_height // 2, goal_width, goal_height)
goal2 = pygame.Rect(screen_width - goal_width, screen_height // 2 - goal_height // 2, goal_width, goal_height)
paddle_size = 30
paddle_velocity = 7
paddle1 = pygame.Rect(screen_width // 2 - 200, screen_height // 2, paddle_size, paddle_size)
paddle2 = pygame.Rect(screen_width // 2 + 200 - paddle_size, screen_height // 2, paddle_size, paddle_size)
disc_size = 50
disc = pygame.Rect(screen_width // 2 - disc_size // 2, screen_height // 2 - disc_size // 2, disc_size, disc_size)
disc_velocity = [7, 7]

# Load images
disc_img = pygame.image.load('disc.png')
blue_paddle_img = pygame.image.load('bluepad.png')
red_paddle_img = pygame.image.load('redpad.png')
background = pygame.image.load('airhockey.png')

# Scores
score1, score2 = 0, 0

def reset_puck():
    global disc_velocity
    disc_velocity = [5, 5]
    disc.x = screen_width // 2 - disc_size // 2
    disc.y = screen_height // 2 - disc_size // 2

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def game_loop():
    global score1, score2

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Player 1 controls (WASD)
        if keys[K_a]:
            paddle1.x -= paddle_velocity
        if keys[K_d]:
            paddle1.x += paddle_velocity
        if keys[K_w]:
            paddle1.y -= paddle_velocity
        if keys[K_s]:
            paddle1.y += paddle_velocity

        # Player 2 controls (Arrow keys)
        if keys[K_LEFT]:
            paddle2.x -= paddle_velocity
        if keys[K_RIGHT]:
            paddle2.x += paddle_velocity
        if keys[K_UP]:
            paddle2.y -= paddle_velocity
        if keys[K_DOWN]:
            paddle2.y += paddle_velocity

        # Boundaries for paddles
        paddle1.x = max(0, min(screen_width // 2 - paddle_size, paddle1.x))
        paddle1.y = max(0, min(screen_height - paddle_size, paddle1.y))
        paddle2.x = max(screen_width // 2, min(screen_width - paddle_size, paddle2.x))
        paddle2.y = max(0, min(screen_height - paddle_size, paddle2.y))

        # Update disc position
        disc.x += disc_velocity[0]
        disc.y += disc_velocity[1]

        # Disc collisions with walls
        if disc.left <= 0 or disc.right >= screen_width:
            disc_velocity[0] *= -1

        if disc.top <= 0 or disc.bottom >= screen_height:
            disc_velocity[1] *= -1

        # Disc collisions with paddles
        if disc.colliderect(paddle1) or disc.colliderect(paddle2):
            disc_velocity[0] *= -1

        # Goal scoring
        if disc.colliderect(goal1):
            score2 += 1
            reset_puck()

        if disc.colliderect(goal2):
            score1 += 1
            reset_puck()

        # Draw everything
        screen.fill(black)
        pygame.draw.rect(screen, light_blue, goal1)
        pygame.draw.rect(screen, light_blue, goal2)
        pygame.draw.rect(screen, white, paddle1)
        pygame.draw.rect(screen, white, paddle2)
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        pygame.draw.circle(screen, white, (screen_width // 2, screen_height // 2), screen_width // 10, 5)
        screen.blit(disc_img, disc)
        screen.blit(blue_paddle_img, (paddle1.x - 5, paddle1.y - 5))
        screen.blit(red_paddle_img, (paddle2.x - 5, paddle2.y - 5))

        draw_text("Player 1: {}".format(score1), white, screen_width // 4, 50)
        draw_text("Player 2: {}".format(score2), white, 3 * screen_width // 4, 50)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
