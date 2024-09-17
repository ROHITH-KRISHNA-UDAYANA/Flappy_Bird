import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (0, 128, 0)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Bird
bird_rect = pygame.Rect(50, HEIGHT // 2 - 10, 30, 30)

# Pipes
pipe_width = 50
pipe_height = random.randint(150, 400)
pipe_x = WIDTH
pipe_gap = 150

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

def draw_bird():
    pygame.draw.circle(screen, WHITE, bird_rect.center, 15)
    pygame.draw.circle(screen, BLACK, (bird_rect.centerx + 5, bird_rect.centery - 5), 5)

def draw_pipes():
    # Draw pipes from bird's perspective
    pygame.draw.rect(screen, PIPE_GREEN, (pipe_x - bird_rect.left + 50, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, PIPE_GREEN, (pipe_x - bird_rect.left + 50, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap))

def check_collision():
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    if bird_rect.right > pipe_x and bird_rect.left < pipe_x + pipe_width:
        if bird_rect.top < pipe_height or bird_rect.bottom > pipe_height + pipe_gap:
            return True
    return False

def update_score():
    global score, high_score
    if pipe_x + pipe_width < bird_rect.left:
        score += 1
        if score > high_score:
            high_score = score

def reset_game():
    global bird_movement, game_active, score, pipe_height, pipe_x
    bird_rect.centery = HEIGHT // 2 - 10
    bird_movement = 0
    game_active = True
    score = 0
    pipe_height = random.randint(150, 400)
    pipe_x = WIDTH

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -6
            if event.key == pygame.K_SPACE and not game_active:
                reset_game()

    screen.fill(SKY_BLUE)

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Draw bird
        draw_bird()

        # Pipe movement
        pipe_x -= 2
        if pipe_x <= -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)

        # Draw pipes
        draw_pipes()

        # Collision detection
        if check_collision():
            game_active = False

        # Update score
        update_score()

    else:
        # Game over screen
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 50))

    pygame.display.update()
    clock.tick(60)

