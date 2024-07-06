import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Crazy Blocks')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Define fonts
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 36)

# Initial position and size of the block
block_x = 350
block_y = 250
block_width = 20  # Adjusted width for smaller block
block_height = 20  # Adjusted height for smaller block
block_speed = 5

# Define game states
HOME = 0
LOADING = 1
PLAYING = 2
game_state = HOME

# Button properties
button_rect = pygame.Rect(300, 250, 200, 100)

# Initialize score and other game variables
score = 0
block_size = 0.1  # Starting block size (very small)
block_max_size = 600  # Maximum block size that fills the screen

# Define levels with obstacles and wall hit requirement
levels = [
    {"name": "Level 1", "duration": 10, "instructions": "Level 1: Hit the walls 10 times to move on.",
     "obstacles": [(200, 200, 100, 100), (500, 350, 50, 50)], "wall_hits_required": 10},
    {"name": "Level 2", "duration": 15, "instructions": "Level 2: Navigate through moving obstacles.",
     "obstacles": [(100, 100, 150, 150), (400, 300, 70, 70), (600, 150, 100, 100)], "wall_hits_required": 15},
    # Add more levels with different obstacles
]
current_level = 0
level_start_time = None

# Wall hit counter
wall_hits = 0

def draw_button(screen, rect, text):
    # Draw button background
    pygame.draw.rect(screen, DARK_GREEN, rect)
    
    # Draw button border
    pygame.draw.rect(screen, GRAY, rect, 4)
    
    # Draw button text
    play_text = button_font.render(text, True, WHITE)
    text_rect = play_text.get_rect(center=rect.center)
    screen.blit(play_text, text_rect)

def draw_text(screen, text, font, color, rect):
    lines = text.split('\n')
    y = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (rect.left, y))
        y += text_surface.get_height() + 5

def draw_progress_bar(screen, progress):
    bar_width = 600
    bar_height = 10
    bar_x = 100
    bar_y = 540
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress * bar_width, bar_height))

    # Draw loading text above the progress bar
    loading_text = text_font.render("LOADING IN PROGRESS", True, WHITE)
    text_rect = loading_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 20))
    screen.blit(loading_text, text_rect)

def draw_ui(screen):
    # Draw score
    score_text = text_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Draw block size indicator
    block_size_text = text_font.render(f"Block Size: {int(block_size * 100)}%", True, WHITE)
    screen.blit(block_size_text, (20, 50))

    # Draw instructions or level information
    if game_state == PLAYING:
        level_info_text = levels[current_level]["instructions"]
    else:
        level_info_text = "Press 'Play' to start"
    draw_text(screen, level_info_text, text_font, WHITE, pygame.Rect(20, 100, 300, 100))

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

# Main game loop
running = True
loading_start_time = None
loading_duration = 5  # Increased duration to 5 seconds for demonstration
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == HOME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = LOADING
                    loading_start_time = time.time()

    if game_state == HOME:
        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the title
        title_text = title_font.render('Crazy Blocks', True, WHITE)
        title_rect = title_text.get_rect(center=(400, 100))
        screen.blit(title_text, title_rect)

        # Draw the "Play" button
        draw_button(screen, button_rect, 'Play')

    elif game_state == LOADING:
        # Fill the screen with black
        screen.fill(BLACK)

        # Display current level information
        draw_text(screen, levels[current_level]["name"], title_font, WHITE, pygame.Rect(50, 50, 700, 100))
        draw_text(screen, levels[current_level]["instructions"], text_font, WHITE, pygame.Rect(50, 150, 700, 300))

        # Update progress bar
        if loading_start_time is not None:
            elapsed_time = time.time() - loading_start_time
            progress = min(elapsed_time / loading_duration, 1)
            draw_progress_bar(screen, progress)
            if elapsed_time >= loading_duration:
                game_state = PLAYING
                level_start_time = time.time()

    elif game_state == PLAYING:
        # Get the current state of all keyboard keys
        keys = pygame.key.get_pressed()

        # Move the block based on key presses
        if keys[pygame.K_LEFT]:
            block_x -= block_speed
        if keys[pygame.K_RIGHT]:
            block_x += block_speed
        if keys[pygame.K_UP]:
            block_y -= block_speed
        if keys[pygame.K_DOWN]:
            block_y += block_speed

        # Ensure the block stays within the window boundaries
        if block_x < 0:
            block_x = 0
            if block_size < block_max_size:
                block_size += 0.1  # Adjusted increment for block size growth
            wall_hits += 1  # Increment wall hit counter
        if block_x > 800 - block_width:
            block_x = 800 - block_width
            if block_size < block_max_size:
                block_size += 0.1  # Adjusted increment for block size growth
            wall_hits += 1  # Increment wall hit counter
        if block_y < 0:
            block_y = 0
            if block_size < block_max_size:
                block_size += 0.1  # Adjusted increment for block size growth
            wall_hits += 1  # Increment wall hit counter
        if block_y > 600 - block_height:
            block_y = 600 - block_height
            if block_size < block_max_size:
                block_size += 0.1  # Adjusted increment for block size growth
            wall_hits += 1  # Increment wall hit counter

        # Update score based on block size
        score = int(block_size)

        # Check if the required number of wall hits is reached
        if wall_hits >= levels[current_level]["wall_hits_required"]:
            # Go to the next level if available
            if current_level + 1 < len(levels):
                current_level += 1
                game_state = LOADING
                loading_start_time = time.time()
                block_size = 0.1  # Reset block size for next level
                block_x = 350  # Reset block position for next level
                block_y = 250
                level_start_time = None
                wall_hits = 0  # Reset wall hit counter for next level
            else:
                # End game or implement game completion logic
                pass

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw UI elements
        draw_ui(screen)

        # Draw obstacles
        draw_obstacles(screen, levels[current_level]["obstacles"])

        # Draw the white block
        pygame.draw.rect(screen, WHITE, (block_x, block_y, int(block_width * block_size), int(block_height * block_size)))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
