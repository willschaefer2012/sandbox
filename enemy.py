import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 255, 0)
ENEMY_SIZE = 30
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (255, 255, 255)
BULLET_SPEED = 10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if self.rect.collidepoint(event.pos):
                self.action()

# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 2 * PLAYER_SIZE
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

enemies = []
enemy_speed = 3
enemy_spawn_timer = 0
enemy_spawn_delay = 60  # Adjust spawn rate as needed

bullets = []
bullet_speed_upgrade_cost = 10
bullet_speed_upgrade_level = 1

score = 0
currency = 0
font = pygame.font.SysFont(None, 36)

# Initialize upgrade variables
damage_upgrade_level = 1
damage_upgrade_cost = 20

# Upgrade functions
def upgrade_bullet_speed():
    global currency, bullet_speed_upgrade_level, bullet_speed_upgrade_cost
    if currency >= bullet_speed_upgrade_cost:
        currency -= bullet_speed_upgrade_cost
        bullet_speed_upgrade_level += 1
        bullet_speed_upgrade_cost += 10  # Increase cost for next level upgrade

def upgrade_damage():
    global currency, damage_upgrade_level, damage_upgrade_cost
    if currency >= damage_upgrade_cost:
        currency -= damage_upgrade_cost
        damage_upgrade_level += 1
        damage_upgrade_cost += 20  # Increase cost for next level upgrade

# Create store buttons
store_buttons = [
    Button(10, 90, 300, 50, f"Upgrade Bullet Speed ({bullet_speed_upgrade_level}): {bullet_speed_upgrade_cost} currency", (0, 100, 200), (0, 150, 255), upgrade_bullet_speed),
    Button(10, 160, 300, 50, f"Upgrade Damage ({damage_upgrade_level}): {damage_upgrade_cost} currency", (0, 100, 200), (0, 150, 255), upgrade_damage)
]

# Store button
store_button = Button(10, 10, 100, 50, "Store", (0, 100, 200), (0, 150, 255), None)

# Game loop
in_store = False
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle events for store button and store buttons
        if not in_store:
            store_button.handle_event(event)
        else:
            for button in store_buttons:
                button.handle_event(event)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
        player_y += player_speed

    player_rect.topleft = (player_x, player_y)

    # Player drawing
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Enemy spawning
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(enemy_rect)
        enemy_spawn_timer = 0

    # Enemy movement and drawing
    for enemy in enemies[:]:
        # Enemy chases the player
        dx = player_x - enemy.x
        dy = player_y - enemy.y
        dist = math.hypot(dx, dy)
        dx = dx / dist if dist else 0
        dy = dy / dist if dist else 0
        enemy.x += dx * enemy_speed
        enemy.y += dy * enemy_speed

        pygame.draw.rect(screen, ENEMY_COLOR, enemy)
        if enemy.x < 0 or enemy.x > SCREEN_WIDTH or enemy.y < 0 or enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Bullet shooting
    if keys[pygame.K_SPACE]:
        bullet = pygame.Rect(player_x + PLAYER_SIZE // 2 - 2, player_y, 4, 10)
        bullets.append(bullet)

    # Bullet movement and collision
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED + bullet_speed_upgrade_level * 2  # Upgradeable bullet speed
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

        # Check collision with enemies
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

        # Remove bullets that go off-screen
        if bullet.y < 0:
            bullets.remove(bullet)

    # Draw score and currency
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    currency_text = font.render(f"Currency: {currency}", True, (255, 255, 255))
    screen.blit(currency_text, (10, 50))

    # Draw store button and handle store logic
    if not in_store:
        store_button.draw(screen)
        if store_button.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                in_store = True
    else:
        for button in store_buttons:
            button.draw(screen)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Game over screen or logic can be added here
