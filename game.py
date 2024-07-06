import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Shooter")

# Player attributes
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - 2 * player_size
player_velocity = 10  # Assigning a default value
player_health = 100

# Weapon attributes
bullet_size = 10
bullet_velocity = 15
bullet_damage = 10
bullets = []

# Enemy attributes
enemies = []
enemy_size = 50
enemy_velocity = 2  # Slower enemy velocity
enemy_health = 50
enemy_spawn_delay = 150  # Delay between enemy spawns in frames (5 seconds at 30 FPS)
enemy_spawn_timer = enemy_spawn_delay

# Game states
game_over = False
cooldown = True
cooldown_timer = 150  # Cooldown timer in frames (5 seconds at 30 FPS)
cooldown_seconds = 5  # Cooldown in seconds
cooldown_countdown = cooldown_seconds * 30  # Cooldown countdown in frames (30 FPS)

# Countdown font
countdown_font = pygame.font.Font(None, 36)
wave_font = pygame.font.Font(None, 48)

# Wave indicator
wave_text = ""
wave_start_time = 0
wave_duration = 2 * 1000  # Wave text duration in milliseconds (2 seconds)

# Shop variables
shop_open = False
shop_button_rect = pygame.Rect(screen_width - 110, 10, 100, 30)
upgrade_button_rects = [
    pygame.Rect(screen_width // 2 - 100, 100, 200, 30),  # Bullet Size
    pygame.Rect(screen_width // 2 - 100, 150, 200, 30),  # Bullet Velocity
    pygame.Rect(screen_width // 2 - 100, 200, 200, 30),  # Player Velocity
]
upgrade_costs = [50, 50, 50]  # Costs for each upgrade
upgrade_descriptions = [
    "Upgrade Bullet Size",
    "Upgrade Bullet Velocity",
    "Upgrade Player Velocity",
]

# Upgrade levels
bullet_size_level = 1
bullet_velocity_level = 1
player_velocity_level = 1

# Points counter
points = 0

# Wave variables
wave = 1
wave_1_enemy_size = 50
wave_1_enemy_health = 50  # Reduced health for Wave 1 enemies
wave_1_enemy_damage = 10
wave_1_triggered = False
wave_1_cooldown = True
wave_1_cooldown_timer = 150  # Cooldown timer in frames (5 seconds at 30 FPS)
wave_1_cooldown_countdown = wave_1_cooldown_timer

wave_2_enemy_size = 70
wave_2_enemy_health = 100  # Reduced health for Wave 2 enemies
wave_2_enemy_damage = 20
wave_2_triggered = False
wave_2_cooldown = True
wave_2_cooldown_timer = 150  # Cooldown timer in frames (5 seconds at 30 FPS)
wave_2_cooldown_countdown = wave_2_cooldown_timer

# Passed enemies counter
enemies_passed = 0
max_passed_enemies = 5

# Create a new enemy
def create_enemy(size, health, damage):
    enemy_x = random.randint(0, screen_width - size)
    enemy_y = random.randint(-screen_height, -size)
    enemies.append([enemy_x, enemy_y, health, size, damage])

# Function to display game over screen
def game_over_screen():
    screen.fill(white)
    font = pygame.font.Font(None, 36)
    text = font.render("You Died", True, black)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
    screen.blit(text, text_rect)

    try_again_text = font.render("Press R to Try Again", True, black)
    try_again_rect = try_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(try_again_text, try_again_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True

# Main game loop
def main():
    global player_health, player_x, player_y, bullets, enemies, game_over
    global cooldown, cooldown_timer, cooldown_countdown, wave_text, points, wave
    global wave_1_triggered, wave_1_cooldown, wave_1_cooldown_countdown
    global wave_2_triggered, wave_2_cooldown, wave_2_cooldown_countdown
    global enemies_passed, bullet_size_level, bullet_velocity_level, player_velocity_level
    global shop_open, shop_button_rect, upgrade_button_rects, upgrade_costs, upgrade_descriptions
    global player_velocity  # Ensure player_velocity is accessible

    while True:
        if game_over:
            if game_over_screen():
                # Reset game variables
                player_health = 100
                player_x = screen_width // 2 - player_size // 2
                player_y = screen_height - 2 * player_size
                bullets = []
                enemies = []
                game_over = False
                cooldown = True
                cooldown_timer = 150  # Reset cooldown timer
                cooldown_countdown = cooldown_seconds * 30  # Reset countdown
                wave_text = ""
                points = 0
                wave = 1
                wave_1_triggered = False
                wave_1_cooldown = True
                wave_1_cooldown_countdown = wave_1_cooldown_timer
                wave_2_triggered = False
                wave_2_cooldown = True
                wave_2_cooldown_countdown = wave_2_cooldown_timer
                enemies_passed = 0  # Reset passed enemies
                # Reset upgrades
                bullet_size_level = 1
                bullet_velocity_level = 1
                player_velocity_level = 1
                player_velocity = 10  # Reset player velocity
            else:
                pygame.quit()
                sys.exit()

        else:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Shoot a bullet
                        bullet_x = player_x + player_size // 2 - bullet_size // 2
                        bullet_y = player_y
                        bullets.append([bullet_x, bullet_y, bullet_damage])

                    # Toggle shop
                    if event.key == pygame.K_s:
                        shop_open = not shop_open

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for button clicks in shop
                    if shop_open:
                        for i, rect in enumerate(upgrade_button_rects):
                            if rect.collidepoint(event.pos):
                                if i == 0 and bullet_size_level < 5 and points >= upgrade_costs[i]:
                                    bullet_size += 5
                                    bullet_size_level += 1
                                    points -= upgrade_costs[i]
                                elif i == 1 and bullet_velocity_level < 5 and points >= upgrade_costs[i]:
                                    bullet_velocity += 5
                                    bullet_velocity_level += 1
                                    points -= upgrade_costs[i]
                                elif i == 2 and player_velocity_level < 5 and points >= upgrade_costs[i]:
                                    player_velocity += 2
                                    player_velocity_level += 1
                                    points -= upgrade_costs[i]

            # Get the state of all keys
            keys = pygame.key.get_pressed()

            # Move the player based on key states
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_velocity
            if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
                player_x += player_velocity
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_velocity
            if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
                player_y += player_velocity

            # Update player health based on collisions with enemies
            for enemy in list(enemies):  # Iterate over a copy of the list
                if (enemy[1] + enemy[3] > player_y and enemy[1] < player_y + player_size) and \
                   (enemy[0] + enemy[3] > player_x and enemy[0] < player_x + player_size):
                    player_health -= enemy[4]
                    enemies.remove(enemy)

            # Fill the screen with white
            screen.fill(white)

            # Draw the player
            pygame.draw.rect(screen, green, (player_x, player_y, player_size, player_size))

            # Draw and move bullets
            for bullet in list(bullets):  # Iterate over a copy of the list
                pygame.draw.rect(screen, red, (bullet[0], bullet[1], bullet_size, bullet_size))
                bullet[1] -= bullet_velocity

                # Remove bullets that go off screen
                if bullet[1] < 0:
                    bullets.remove(bullet)

            # Spawn enemies on a delay
            if not cooldown:
                if wave == 1 and len(enemies) == 0 and wave_1_cooldown:
                    wave_text = "Wave 1"
                    wave_start_time = pygame.time.get_ticks()
                    wave_1_cooldown = False
                elif wave == 2 and len(enemies) == 0 and wave_2_cooldown:
                    wave_text = "Wave 2"
                    wave_start_time = pygame.time.get_ticks()
                    wave_2_cooldown = False
                else:
                    if wave == 1:
                        enemy_spawn_delay = wave_1_enemy_size * 3
                    if wave == 2:
                        enemy_spawn_delay = 0

                    if enemy_spawn_timer <= 0:
                        enemy_size = wave_1_enemy_size if wave == 1 else wave_2_enemy_size
                        enemy_health = wave_1_enemy_health if wave == 1 else wave_2_enemy_health
                        enemy_damage = wave_1_enemy_damage if wave == 1 else wave_2_enemy_damage
                        create_enemy(enemy_size, enemy_health, enemy_damage)
                        enemy_spawn_timer = enemy_spawn_delay
                    else:
                        enemy_spawn_timer -= 1

            # Draw and move enemies
            for enemy in list(enemies):  # Iterate over a copy of the list
                pygame.draw.rect(screen, black, (enemy[0], enemy[1], enemy[3], enemy[3]))
                enemy[1] += enemy_velocity

                # Remove enemies that go off screen
                if enemy[1] > screen_height:
                    enemies.remove(enemy)
                    enemies_passed += 1  # Increment passed enemies counter
                    if enemies_passed > max_passed_enemies:
                        player_health = 0  # Player dies if more than 5 enemies pass

            # Handle wave transitions
            if wave == 1 and len(enemies) == 0 and not wave_1_cooldown:
                wave += 1
                wave_1_cooldown = True
                cooldown = True
                cooldown_timer = 150  # Reset cooldown timer
                cooldown_countdown = cooldown_seconds * 30  # Reset countdown for next wave

            elif wave == 2 and len(enemies) == 0 and not wave_2_cooldown:
                wave += 1
                wave_2_cooldown = True
                cooldown = True
                cooldown_timer = 150  # Reset cooldown timer
                cooldown_countdown = cooldown_seconds * 30  # Reset countdown for next wave

            # Draw health bar
            pygame.draw.rect(screen, black, (screen_width - 210, screen_height - 30, 200, 20))
            pygame.draw.rect(screen, green, (screen_width - 210, screen_height - 30, player_health * 2, 20))

            # Draw wave indicator
            if wave_text:
                current_time = pygame.time.get_ticks()
                if current_time - wave_start_time < wave_duration:
                    wave_text_rendered = wave_font.render(wave_text, True, black)
                    wave_text_rect = wave_text_rendered.get_rect(center=(screen_width // 2, 50))
                    screen.blit(wave_text_rendered, wave_text_rect)
                else:
                    wave_text = ""

            # Draw shop button
            pygame.draw.rect(screen, (0, 255, 255), shop_button_rect)
            shop_text = pygame.font.Font(None, 36).render("Shop (S)", True, black)
            screen.blit(shop_text, (screen_width - 105, 15))

            # Draw points counter in shop
            points_text = pygame.font.Font(None, 24).render(f"Points: {points}", True, black)
            screen.blit(points_text, (20, 20))

            # Draw upgrade buttons and costs
            if shop_open:
                for i, rect in enumerate(upgrade_button_rects):
                    pygame.draw.rect(screen, (255, 255, 0), rect)
                    upgrade_text = pygame.font.Font(None, 24).render(f"{upgrade_descriptions[i]} - Cost: {upgrade_costs[i]}", True, black)
                    screen.blit(upgrade_text, (rect.x + 10, rect.y + 5))

            # Check if game over
            if player_health <= 0:
                game_over = True

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
