import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Military Game")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.original_image = self.image.copy()  # Original image for health bar adjustment
        self.health = 100  # Health attribute
        self.max_health = 100  # Maximum health attribute
    
    def update(self):
        # Basic animation: move towards target x position
        if self.rect.centerx < self.target_x:
            self.rect.centerx += 1
        elif self.rect.centerx > self.target_x:
            self.rect.centerx -= 1
        
        # Update health bar
        self.image = self.original_image.copy()
        health_width = int(self.rect.width * (self.health / self.max_health))
        pygame.draw.rect(self.image, RED, (0, self.rect.height + 5, self.rect.width, 10))
        pygame.draw.rect(self.image, GREEN, (0, self.rect.height + 5, health_width, 10))

# Create blocks
red_block = Block(RED, 50, 50, screen_width // 4, screen_height // 2)
green_block = Block(GREEN, 50, 50, 3 * screen_width // 4, screen_height // 2)

# Group for all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(red_block, green_block)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update game state
    all_sprites.update()  # Update block positions
    
    # Render graphics
    screen.fill((0, 0, 0))  # Fill screen with black
    all_sprites.draw(screen)  # Draw all sprites
    
    # Update display
    pygame.display.flip()
    pygame.time.delay(10)  # Optional delay to control animation speed

# Quit Pygame
pygame.quit()
sys.exit()
