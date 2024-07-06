import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
COIN_SIZE = 30
COIN_COUNT = 5
COIN_SPEED = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Pygame Game')

# Player object
player = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)
player_color = RED

# Coins list
coins = []
for _ in range(COIN_COUNT):
    coin = pygame.Rect(random.randint(0, SCREEN_WIDTH - COIN_SIZE),
                       random.randint(0, SCREEN_HEIGHT - COIN_SIZE),
                       COIN_SIZE, COIN_SIZE)
    coins.append(coin)

def draw_objects():
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, player)
    for coin in coins:
        pygame.draw.ellipse(screen, YELLOW, coin)

def move_coins():
    for coin in coins:
        coin.y += COIN_SPEED
        if coin.top > SCREEN_HEIGHT:
            coin.y = 0
            coin.x = random.randint(0, SCREEN_WIDTH - COIN_SIZE)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[K_RIGHT] and player.right < SCREEN_WIDTH:
        player.x += 5
    if keys[K_UP] and player.top > 0:
        player.y -= 5
    if keys[K_DOWN] and player.bottom < SCREEN_HEIGHT:
        player.y += 5

    move_coins()

    # Check for collision with coins
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)  # Remove the coin from the list
            # Add scoring logic or any other action here

    draw_objects()
    pygame.display.update()
    clock.tick(30)
