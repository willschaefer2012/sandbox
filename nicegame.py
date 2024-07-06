import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
player_size = 50
player_color = BLUE
player_pos = [WIDTH // 2, HEIGHT - player_size]
player_speed = 5
player_vel_y = 0
jump_power = -15
gravity = 0.8

# Platform settings
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(150, 450, 200, 20),
    pygame.Rect(400, 350, 200, 20),
    pygame.Rect(650, 250, 150, 20),
]

def draw_player(screen, pos):
    pygame.draw.rect(screen, player_color, (*pos, player_size, player_size))

def draw_platforms(screen, platforms):
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

def player_movement(keys, pos, vel_y):
    if keys[pygame.K_LEFT]:
        pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        pos[0] += player_speed
    pos[1] += vel_y
    return pos

def check_collision(player_rect, platforms):
    for platform in platforms:
        if player_rect.colliderect(platform) and player_rect.bottom <= platform.bottom:
            return platform.top
    return None

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Jumping
    if keys[pygame.K_SPACE] and player_pos[1] + player_size >= HEIGHT - 40:
        player_vel_y = jump_power

    # Apply gravity
    player_vel_y += gravity

    # Move player
    player_pos = player_movement(keys, player_pos, player_vel_y)

    # Collision detection
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    collision_platform_top = check_collision(player_rect, platforms)
    if collision_platform_top is not None:
        player_pos[1] = collision_platform_top - player_size
        player_vel_y = 0

    # Prevent going out of bounds
    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size
    if player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size
        player_vel_y = 0

    # Drawing
    screen.fill(WHITE)
    draw_player(screen, player_pos)
    draw_platforms(screen, platforms)
    pygame.display.flip()

    clock.tick(30)
