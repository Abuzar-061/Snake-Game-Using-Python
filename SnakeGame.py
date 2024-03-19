import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Speed of the game
speed = 15

# Window size
frame_size_x = 720
frame_size_y = 480

# Initialize game window
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption("Snake Game")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Frame per second controller
fps_controller = pygame.time.Clock()

# Snake settings
square_size = 20

# Initialize game variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "Right"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0

# Function to display score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)

# Initialize variables
init_vars()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord("w"):
                if direction != "DOWN":
                    direction = "UP"
            elif event.key == pygame.K_DOWN or event.key == ord("s"):
                if direction != "UP":
                    direction = "DOWN"
            elif event.key == pygame.K_LEFT or event.key == ord("a"):
                if direction != "RIGHT":
                    direction = "LEFT"
            elif event.key == pygame.K_RIGHT or event.key == ord("d"):
                if direction != "LEFT":
                    direction = "RIGHT"

    # Move the snake
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    # Check boundaries
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] >= frame_size_x:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] >= frame_size_y:
        head_pos[1] = 0

    # Eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Food Spawn
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                    random.randrange(1, (frame_size_y // square_size)) * square_size]
        food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0] + 2, pos[1] + 2, square_size - 2, square_size))

    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))

    # Game Over Condition
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            init_vars()

    # Show score
    show_score(1, white, 'Consolas', 20)

    # Update display
    pygame.display.update()

    # Control game speed
    fps_controller.tick(speed)