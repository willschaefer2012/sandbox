import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Player variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 50
player_speed = 5

# Gun variables
bullet_speed = 7
bullets = []
bullet_radius = 5

# Friend variables
friend_x = random.randint(50, SCREEN_WIDTH - 50)
friend_y = random.randint(50, SCREEN_HEIGHT - 50)
friend_radius = 20

# Enemy variables
enemies = []
enemy_speed = 3
enemy_radius = 15
enemy_spawn_rate = 1  # Number of enemies spawned per second

# Hostage variables
hostage_x = random.randint(50, SCREEN_WIDTH - 50)
hostage_y = random.randint(50, SCREEN_HEIGHT - 50)
hostage_radius = 20
hostage_taken = False

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not hostage_taken:
                # Calculate bullet direction towards the mouse position
                bullet_angle = math.atan2(pygame.mouse.get_pos()[1] - player_y, pygame.mouse.get_pos()[0] - player_x)
                bullet_dx = bullet_speed * math.cos(bullet_angle)
                bullet_dy = bullet_speed * math.sin(bullet_angle)
                bullets.append((player_x, player_y, bullet_dx, bullet_dy))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT:
        player_y += player_speed

    # Update bullets
    for bullet in bullets[:]:
        bullet_x, bullet_y, bullet_dx, bullet_dy = bullet
        bullet_x += bullet_dx
        bullet_y += bullet_dy
        if bullet_x < 0 or bullet_x > SCREEN_WIDTH or bullet_y < 0 or bullet_y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:
            bullet = (bullet_x, bullet_y, bullet_dx, bullet_dy)
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy[0] - enemy_radius, enemy[1] - enemy_radius, 2 * enemy_radius, 2 * enemy_radius)
                if enemy_rect.collidepoint(bullet_x, bullet_y):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break
            pygame.draw.circle(screen, WHITE, (int(bullet_x), int(bullet_y)), bullet_radius)

    # Spawn enemies
    if random.random() < enemy_spawn_rate / FPS and not hostage_taken:
        enemy_x = random.randint(50, SCREEN_WIDTH - 50)
        enemy_y = random.randint(50, SCREEN_HEIGHT - 50)
        enemies.append((enemy_x, enemy_y))

    # Update enemies
    for enemy in enemies[:]:
        enemy_x, enemy_y = enemy
        if enemy_y < SCREEN_HEIGHT:
            enemy_y += enemy_speed
        else:
            enemies.remove(enemy)

    # Collision detection
    player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)
    friend_rect = pygame.Rect(friend_x - friend_radius, friend_y - friend_radius, 2 * friend_radius, 2 * friend_radius)
    hostage_rect = pygame.Rect(hostage_x - hostage_radius, hostage_y - hostage_radius, 2 * hostage_radius, 2 * hostage_radius)

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0] - enemy_radius, enemy[1] - enemy_radius, 2 * enemy_radius, 2 * enemy_radius)
        if enemy_rect.colliderect(player_rect):
            enemies.remove(enemy)
            # Handle game over or score deduction for friendly fire
        elif enemy_rect.colliderect(friend_rect):
            enemies.remove(enemy)
            # Handle enemy attack on friend
        elif enemy_rect.colliderect(hostage_rect) and not hostage_taken:
            enemies.remove(enemy)
            hostage_taken = True
            # Handle hostage taken scenario

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN, (friend_x, friend_y), friend_radius)
    pygame.draw.circle(screen, BLUE, (player_x, player_y), 20)
    pygame.draw.circle(screen, RED, (hostage_x, hostage_y), hostage_radius)

    for enemy in enemies:
        pygame.draw.circle(screen, RED, enemy, enemy_radius)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
