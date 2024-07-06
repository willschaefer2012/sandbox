import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMY_COUNT = 5
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 7
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Load images
player_img = pygame.image.load('soldier.png')
enemy_img = pygame.image.load('theif-png.png')
bullet_img = pygame.image.load('bullet.png')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game variables
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_rect = player_img.get_rect(center=(player_x, player_y))

enemies = []
for _ in range(ENEMY_COUNT):
    enemy_x = random.randint(50, SCREEN_WIDTH - 50)
    enemy_y = random.randint(50, SCREEN_HEIGHT // 2)
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_img.get_width(), enemy_img.get_height()))

bullets = []
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_rect.width:
        player_x += PLAYER_SPEED

    # Shooting mechanic
    if keys[pygame.K_SPACE]:
        bullet_rect = bullet_img.get_rect(center=(player_x + player_rect.width // 2, player_y))
        bullets.append(bullet_rect)

    # Update and draw bullets
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        screen.blit(bullet_img, bullet)
        if bullet.y < 0:
            bullets.remove(bullet)

    # Update and draw enemies
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
        screen.blit(enemy_img, enemy)

        # Collision detection: Bullet hits enemy
        for bullet in bullets:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

        # Game over condition: Enemy reaches bottom of the screen
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)
            score -= 5

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()
