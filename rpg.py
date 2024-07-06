import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_WIDTH, TILE_HEIGHT = 64, 32

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pseudo-3D RPG")

# Load player image
player_image = pygame.image.load("player.png").convert_alpha()
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= 5
    if keys[pygame.K_s]:
        player_y += 5
    if keys[pygame.K_a]:
        player_x -= 5
    if keys[pygame.K_d]:
        player_x += 5

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
