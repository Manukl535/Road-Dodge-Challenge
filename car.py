import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions (reduced size)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_GRAY = (105, 105, 105)
DARK_YELLOW = (128, 128, 0)
BLUE = (0, 0, 128)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)

# Initialize game variables
FPS = 60
player_speed = 5
enemy_speed = 5
score = 0
game_over = False
show_instructions = True  # Initially show instructions

# Road dimensions
ROAD_WIDTH = 300
LANE_WIDTH = 75
LANE_OFFSET = (SCREEN_WIDTH - ROAD_WIDTH) // 2

# Car dimensions
CAR_WIDTH = 45
CAR_HEIGHT = 90
player_car_x = LANE_OFFSET + (ROAD_WIDTH - CAR_WIDTH) // 2
player_car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20

# Enemy car dimensions and variables
ENEMY_CAR_WIDTH = 45
ENEMY_CAR_HEIGHT = 90
enemy_car_x = LANE_OFFSET + random.choice([0, 75, 150, 225])
enemy_car_y = -ENEMY_CAR_HEIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load car image
player_car_image = pygame.image.load('car.png')
player_car_image = pygame.transform.scale(player_car_image, (CAR_WIDTH, CAR_HEIGHT))

# Load enemy car image
enemy_car_image = pygame.image.load('enemy_car.png')
enemy_car_image = pygame.transform.scale(enemy_car_image, (ENEMY_CAR_WIDTH, ENEMY_CAR_HEIGHT))

# Font setup
font_large = pygame.font.SysFont(None, 36)  # Larger font size for headings
font_small = pygame.font.SysFont(None, 24)  # Smaller font size for instructions

# Function to handle events
def handle_events():
    global game_over, player_car_x, show_instructions

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and show_instructions:
                show_instructions = False  # Start game on space bar press
            elif event.key == pygame.K_ESCAPE and game_over:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_car_x < LANE_OFFSET + ROAD_WIDTH - CAR_WIDTH:
        player_car_x += player_speed
    if keys[pygame.K_LEFT] and player_car_x > LANE_OFFSET:
        player_car_x -= player_speed

# Function to generate enemy car
def generate_enemy_car():
    global enemy_car_x, enemy_car_y
    if enemy_car_y > SCREEN_HEIGHT:
        enemy_car_y = -ENEMY_CAR_HEIGHT
        enemy_car_x = LANE_OFFSET + random.choice([0, 75, 150, 225])

# Function to move enemy car
def move_enemy_car():
    global enemy_car_x, enemy_car_y, score, game_over, player_car_x, player_car_y

    enemy_car_y += enemy_speed
    if enemy_car_y > SCREEN_HEIGHT:
        enemy_car_y = -ENEMY_CAR_HEIGHT
        enemy_car_x = LANE_OFFSET + random.choice([0, 75, 150, 225])
        score += 1

    # Check collision
    if enemy_car_y + ENEMY_CAR_HEIGHT > player_car_y and enemy_car_y < player_car_y + CAR_HEIGHT:
        if player_car_x < enemy_car_x + ENEMY_CAR_WIDTH and player_car_x + CAR_WIDTH > enemy_car_x:
            game_over = True

# Function to draw background
def draw_background():
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, GRAY, [LANE_OFFSET, 0, ROAD_WIDTH, SCREEN_HEIGHT])
    pygame.draw.line(screen, WHITE, [LANE_OFFSET + ROAD_WIDTH // 2, 0], [LANE_OFFSET + ROAD_WIDTH // 2, SCREEN_HEIGHT], 4)

# Function to draw player car
def draw_player_car():
    screen.blit(player_car_image, (player_car_x, player_car_y))

# Function to draw enemy car
def draw_enemy_car():
    screen.blit(enemy_car_image, (enemy_car_x, enemy_car_y))

# Function to display game over
def display_game_over():
    game_over_text = font_large.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

# Function to display instructions
def display_instructions():
    instruction_lines = []
    
    if show_instructions:
        instruction_lines.append("Press SPACE to Start")
        instruction_lines.append("Use Arrow Keys to Move")
        instruction_lines.append("Press ESC to Exit")
    elif game_over:
        instruction_lines.append("Press R to Restart")
        instruction_lines.append("Press ESC to Exit")
    
    for i, line in enumerate(instruction_lines):
        if i == 0:
            text = font_large.render(line, True, WHITE)
        else:
            text = font_small.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30))
        screen.blit(text, text_rect)

# Function to restart the game
def restart_game():
    global score, game_over, player_car_x, player_car_y, enemy_car_x, enemy_car_y

    score = 0
    game_over = False
    player_car_x = LANE_OFFSET + (ROAD_WIDTH - CAR_WIDTH) // 2
    player_car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    enemy_car_x = LANE_OFFSET + random.choice([0, 75, 150, 225])
    enemy_car_y = -ENEMY_CAR_HEIGHT

# Main game loop
def main():
    global game_over, show_instructions

    clock = pygame.time.Clock()

    while True:
        handle_events()

        screen.fill(DARK_GREEN)

        if not game_over and not show_instructions:
            generate_enemy_car()
            move_enemy_car()
            draw_background()
            draw_player_car()
            draw_enemy_car()
            display_score()
        else:
            display_instructions()

            if game_over:
                display_game_over()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart_game()

        pygame.display.update()
        clock.tick(FPS)

# Function to display score
def display_score():
    score_text = font_small.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

if __name__ == "__main__":
    main()  # Start main loop
