"""
Simple Racing Game
===================

Instructions:
- Use the LEFT and RIGHT arrow keys to steer your car.
- Avoid the obstacles (gray rectangles) that move down the screen.
- The goal is to survive as long as possible while avoiding collisions with the obstacles.
- The game ends when your car collides with an obstacle.

Controls:
- LEFT Arrow: Move the car left.
- RIGHT Arrow: Move the car right.
- Press ENTER at the main menu to start the game.
- Press ESC to quit the game at the main menu.

Scoring:
- Your score increases by 1 point for each frame you survive.

Enjoy the game!
"""


import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)  # For obstacles

# Font settings
font = pygame.font.SysFont(None, 55)

# Car settings
CAR_WIDTH, CAR_HEIGHT = 50, 100
car_color = RED
car_rect = pygame.Rect(WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)
car_speed = 5

# Obstacle settings
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 100  # Match the car dimensions for obstacles
obstacle_color = GRAY
obstacle_speed = 5
obstacles = []  # Initialize obstacles globally

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Function to create a new obstacle
def create_obstacle():
    x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    y = -OBSTACLE_HEIGHT
    return pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Function to move obstacles
def move_obstacles(obstacles):
    for obs in obstacles:
        obs.y += obstacle_speed
    return [obs for obs in obstacles if obs.y < HEIGHT]

# Function to check for collisions
def check_collision(car_rect, obstacles):
    for obs in obstacles:
        if car_rect.colliderect(obs):
            return True
    return False

# Function to display text
def display_text(text, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to draw the player car
def draw_car(rect):
    pygame.draw.rect(screen, car_color, rect)  # Car body
    # Car windows
    pygame.draw.rect(screen, WHITE, pygame.Rect(rect.x + 10, rect.y + 10, 30, 15))
    pygame.draw.rect(screen, WHITE, pygame.Rect(rect.x + 10, rect.y + 30, 30, 15))
    # Car wheels (4 vertical ellipses)
    wheel_width = 20
    wheel_height = 40
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x - 15, rect.bottom - 35, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x + CAR_WIDTH - 2, rect.bottom - 35, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x - 15, rect.bottom - 105, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x + CAR_WIDTH - 2, rect.bottom - 105, wheel_width, wheel_height))

# Function to draw an obstacle car
def draw_obstacle(rect):
    pygame.draw.rect(screen, obstacle_color, rect)  # Obstacle body
    # Obstacle windows
    pygame.draw.rect(screen, WHITE, pygame.Rect(rect.x + 10, rect.y + 50, 30, 15))
    pygame.draw.rect(screen, WHITE, pygame.Rect(rect.x + 10, rect.y + 70, 30, 15))
    # Obstacle wheels (4 vertical ellipses)
    wheel_width = 20
    wheel_height = 40
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x - 15, rect.bottom - 35, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x + CAR_WIDTH - 2, rect.bottom - 35, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x - 15, rect.bottom - 105, wheel_width, wheel_height))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(rect.x + CAR_WIDTH - 2, rect.bottom - 105, wheel_width, wheel_height))


# Function to display the main menu
def main_menu():
    while True:
        screen.fill(WHITE)
        display_text("Simple Racing Game", BLACK, 55, WIDTH // 2, HEIGHT // 2 - 100)
        display_text("Press ENTER to Start", BLACK, 35, WIDTH // 2, HEIGHT // 2)
        display_text("Press ESC to Quit", BLACK, 35, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Start the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Game loop
def game_loop():
    global obstacles  # Declare that we're using the global variable
    obstacle_timer = 0
    score = 0
    car_rect.topleft = (WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 10)
    obstacles.clear()  # Clear obstacles
    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= car_speed
        if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
            car_rect.x += car_speed
        
        # Spawn new obstacles
        obstacle_timer += 1
        if obstacle_timer > 20:
            obstacle_timer = 0
            obstacles.append(create_obstacle())
        
        # Move obstacles
        obstacles = move_obstacles(obstacles)
        
        # Check for collisions
        if check_collision(car_rect, obstacles):
            screen.fill(WHITE)
            display_text(f"Game Over! Your score: {score}", RED, 55, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds before quitting
            return  # Return to the main menu
        
        # Draw everything
        draw_car(car_rect)  # Draw the player car
        for obs in obstacles:
            draw_obstacle(obs)  # Draw the obstacles
        
        # Display score
        display_text(f"Score: {score}", BLACK, 35, WIDTH // 2, 30)
        
        # Update display
        pygame.display.flip()
        
        # Increment score
        score += 1
        
        # Cap the frame rate
        clock.tick(FPS)

# Main loop
while True:
    main_menu()  # Show the main menu
    game_loop()  # Start the game
