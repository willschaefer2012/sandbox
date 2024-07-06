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
SHARK_SIZE = 100  # Increased shark size
SHARK_COUNT = 5
SHARK_SPEED = 3

# Health constants
SHARK_MAX_HEALTH = 200
SHARK_DAMAGE = 10  # Damage sharks deal to the player
PLAYER_MAX_HEALTH = 100

# Player health
player_health = PLAYER_MAX_HEALTH

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load the sky image
sky_image = pygame.image.load('why-is-sky-blue.jpg')  # Replace with your actual sky image file path
sky_image = pygame.transform.scale(sky_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the shark image
shark_image = pygame.image.load('shark.png')  # Replace with your actual shark image file path
shark_image = pygame.transform.scale(shark_image, (SHARK_SIZE, SHARK_SIZE))

# Load the chainsaw image
chainsaw_image = pygame.image.load('chainsaw.png')  # Replace with your actual chainsaw image file path
chainsaw_image = pygame.transform.scale(chainsaw_image, (PLAYER_SIZE, PLAYER_SIZE))

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Pygame Game')

# Player object
player = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE)

# Weapon class
class Weapon:
    def __init__(self, name, image_path, damage, cost, max_health):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.damage = damage
        self.cost = cost
        self.max_health = max_health
        self.health = max_health  # Start with full health

    def draw_health_bar(self, x, y):
        length = 50
        height = 5
        fill = (self.health / self.max_health) * length
        border_rect = pygame.Rect(x, y, length, height)
        fill_rect = pygame.Rect(x, y, fill, height)

        # Draw border of the health bar
        pygame.draw.rect(screen, BLACK, border_rect, 1)

        # Draw filled portion of the health bar
        if self.health > 0:
            pygame.draw.rect(screen, GREEN, fill_rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0

    def is_active(self):
        return self.health > 0

# Initialize weapons
weapons = [
    Weapon("Chainsaw", 'chainsaw.png', 50, 0, 500),  # Increased damage
    Weapon("Upgraded Chainsaw", 'chainsaw.png', 50, 100, 500),
    Weapon("Super Chainsaw", 'chainsaw.png', 50, 200, 500),
]

# Current weapon
current_weapon_index = 0
current_weapon = weapons[current_weapon_index]

# Currency
currency = 0

# Function to create sharks
def create_sharks(count):
    sharks_list = []
    for _ in range(count):
        shark = {
            'rect': pygame.Rect(random.randint(0, SCREEN_WIDTH - SHARK_SIZE),
                                random.randint(0, SCREEN_HEIGHT - SHARK_SIZE),
                                SHARK_SIZE, SHARK_SIZE),
            'health': SHARK_MAX_HEALTH
        }
        sharks_list.append(shark)
    return sharks_list

# Initialize sharks
sharks = create_sharks(SHARK_COUNT)

# Counter for collected sharks
shark_counter = 0

# Shop class
class Shop:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)
        self.visible = False
        self.message = ""

    def draw(self):
        if not self.visible:
            return
        shop_rect = pygame.Rect(100, 100, 600, 400)
        pygame.draw.rect(screen, WHITE, shop_rect)
        pygame.draw.rect(screen, BLACK, shop_rect, 2)
        self.draw_text("Shop", 50, SCREEN_WIDTH // 2, 120, BLACK)
        for i, weapon in enumerate(weapons):
            self.draw_text(f"{weapon.name}: {weapon.cost} currency", 30, 150, 180 + i * 40, BLACK)
        self.draw_text("Press 1, 2, 3 to buy respective weapons", 30, 150, 360, BLACK)
        self.draw_text(f"Currency: {currency}", 30, 150, 400, BLACK)
        if self.message:
            self.draw_text(self.message, 30, SCREEN_WIDTH // 2, 440, BLACK)

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def purchase_weapon(self, index):
        global currency, current_weapon_index, current_weapon
        if index < len(weapons) and currency >= weapons[index].cost:
            currency -= weapons[index].cost
            current_weapon_index = index
            current_weapon = weapons[current_weapon_index]
            self.message = f"Purchased {weapons[index].name}"
        else:
            self.message = "Not enough currency"

shop = Shop()

def draw_objects():
    screen.blit(sky_image, (0, 0))  # Draw sky image as the background
    screen.blit(current_weapon.image, player.topleft)  # Draw the current weapon image
    current_weapon.draw_health_bar(player.left, player.top - 15)  # Draw the chainsaw health bar
    for shark in sharks:
        screen.blit(shark_image, shark['rect'].topleft)  # Draw the shark image
        draw_health_bar(shark['rect'].left, shark['rect'].top - 15, shark['health'])  # Draw the health bar above the shark
    draw_text(f'Sharks: {shark_counter}', 30, 20, 20, BLACK)
    draw_text(f'Currency: {currency}', 30, 20, 60, BLACK)
    draw_text(f'Player Health: {player_health}', 30, 20, 100, BLACK)
    draw_text('Press "O" to open/close the shop', 30, 20, 140, BLACK)
    shop.draw()

def draw_text(text, size, x, y, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_health_bar(x, y, health):
    length = 100
    height = 10
    fill = (health / SHARK_MAX_HEALTH) * length
    border = pygame.Rect(x, y, length, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(screen, BLACK, border, 2)
    if health > 0:
        pygame.draw.rect(screen, RED, fill_rect)

def draw_player_health_bar():
    length = 200
    height = 20
    fill = (player_health / PLAYER_MAX_HEALTH) * length
    border = pygame.Rect(20, SCREEN_HEIGHT - 40, length, height)
    fill_rect = pygame.Rect(20, SCREEN_HEIGHT - 40, fill, height)
    pygame.draw.rect(screen, BLACK, border, 2)
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, fill_rect)

def move_sharks():
    for shark in sharks:
        shark['rect'].x += random.choice([-SHARK_SPEED, SHARK_SPEED])
        shark['rect'].y += random.choice([-SHARK_SPEED, SHARK_SPEED])
        
        # Keep sharks within screen boundaries
        if shark['rect'].left < 0:
            shark['rect'].left = 0
        if shark['rect'].right > SCREEN_WIDTH:
            shark['rect'].right = SCREEN_WIDTH
        if shark['rect'].top < 0:
            shark['rect'].top = 0
        if shark['rect'].bottom > SCREEN_HEIGHT:
            shark['rect'].bottom = SCREEN_HEIGHT

# Main game loop
clock = pygame.time.Clock()
shop_toggle_delay = 300  # Delay in milliseconds for toggling the shop
last_shop_toggle = 0
chainsaw_hits = 0  # Counter for chainsaw hits on sharks

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    if keys[K_o] and current_time - last_shop_toggle > shop_toggle_delay:  # Press 'O' to open/close the shop
        shop.visible = not shop.visible
        last_shop_toggle = current_time

    if not
