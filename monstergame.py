import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monster Fighter")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up the player
player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 10
player_health = 500

# Set up the sword
sword_img = pygame.image.load('slasher.png')
sword_img = pygame.transform.scale(sword_img, (100, 100))
sword_durability = 1000  # Initial sword durability
sword_max_durability = 1000  # Maximum durability of the sword
sword_regeneration_rate = 1  # Rate at which sword regenerates per frame
sword_pos_offset = [40, -80]  # Offset to position the sword relative to the player
sword_pos = [0, 0]  # Sword position, updated later

# Set up the healer
healer_size = 50
healer_pos = [random.randint(0, screen_width - healer_size), random.randint(0, screen_height - healer_size)]
healer_health_restore = 100

# Set up the score
score = 0
font = pygame.font.SysFont("monospace", 35)
bold_font = pygame.font.SysFont("monospace", 35, bold=True)

# List to store monsters
monsters = []

# Game parameters
current_level = 1
monster_size = 50  # Size of the monsters
monster_spawn_rate = 180  # 60 frames per second * 3 seconds
monster_spawn_timer = 0  # Timer for monster spawning
monster_damage = 50  # Increased damage to sword

# Track waves
wave_count = 1
monsters_defeated = 0
monsters_per_wave = 10
cooldown_time = 5  # Cooldown time in seconds
cooldown_start_time = 0
cooldown_active = False

# Track monsters slain
monsters_slain = 0

# Function to display text
def display_text(text, size, color, x, y, font):
    label = font.render(text, True, color)
    text_width, text_height = font.size(text)
    screen.blit(label, (x - text_width // 2, y - text_height // 2))

# Function to draw the health bar
def draw_health_bar(health, x, y, width, height, label):
    fill = (health / 500) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)
    display_text(label, 20, BLACK, x + width // 2, y - 20, font)

# Function to draw the sword's health bar
def draw_sword_health_bar(current_durability, max_durability, x, y, width, height, label):
    fill = (current_durability / max_durability) * width
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)
    display_text(label, 20, BLACK, x + width // 2, y - 20, font)

# Function to draw the healer
def draw_healer():
    pygame.draw.rect(screen, YELLOW, (*healer_pos, healer_size, healer_size))

# Function to display the current wave number
def display_wave_number(wave):
    display_text(f"Wave {wave}", 40, BLACK, screen_width // 2, screen_height // 2, font)

# Function to display monsters slain count
def display_monsters_slain(count):
    display_text(f"Monsters Slain: {count}", 20, BLACK, screen_width - 150, screen_height - 40, bold_font)

# Game over screen
def game_over_screen(final_score):
    screen.fill(WHITE)
    display_text("Game Over", 50, BLACK, screen_width // 2, 250, font)
    display_text(f"Final Score: {final_score}", 30, BLACK, screen_width // 2, 350, font)
    display_text("Press any key to restart", 30, BLACK, screen_width // 2, 450, font)
    pygame.display.flip()
    wait_for_keypress()

# Function to wait for a key press
def wait_for_keypress():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Function to spawn a new monster
def spawn_monster():
    monster_speed = random.uniform(0.2, 0.6) * 3  # Multiply speed by 3 to make monsters faster
    new_monster = {
        'pos': [random.randint(0, screen_width - monster_size), random.randint(-screen_height, 0)],
        'speed': monster_speed,
    }
    monsters.append(new_monster)

# Function to update positions of monsters and handle collisions
def update_monster_positions():
    global player_health, monsters_defeated, score, monsters_slain, game_active, monster_spawn_timer

    for monster in monsters:
        monster_pos_x, monster_pos_y = monster['pos']
        player_pos_x, player_pos_y = player_pos

        # Calculate direction towards player
        direction_x = player_pos_x - monster_pos_x
        direction_y = player_pos_y - monster_pos_y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        monster['pos'][0] += int(direction_x * monster['speed'])
        monster['pos'][1] += int(direction_y * monster['speed'])

        # Check for collision with player
        if (monster_pos_y + monster_size > player_pos_y and
                (player_pos_x < monster_pos_x < player_pos_x + player_size or
                 player_pos_x < monster_pos_x + monster_size < player_pos_x + player_size)):
            player_health -= monster_damage
            if player_health <= 0:
                game_active = False

            # Remove the monster after collision
            monsters.remove(monster)

            # Increase monsters defeated count
            monsters_defeated += 1

        # Remove monsters that have reached the bottom of the screen
        if monster_pos_y > screen_height:
            monsters.remove(monster)
            score += 1
            monsters_defeated += 1

    return game_active

def main():
    global player_pos, player_health, score, monsters, attacking, monsters_slain, wave_count, cooldown_start_time, cooldown_active, sword_durability, sword_max_durability, monster_spawn_timer

    running = True
    while running:
        # Reset game variables
        player_pos = [screen_width // 2, screen_height - 2 * player_size]
        player_health = 500
        score = 0
        monsters = []
        attacking = False
        monsters_slain = 0
        monster_spawn_timer = 0

        # Display wave number before starting the game
        display_wave_number(wave_count)
        pygame.display.flip()
        pygame.time.delay(3000)  # Delay for 3 seconds before starting the game

        game_active = True
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:  # Move up
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:  # Move down
                player_pos[1] += player_speed

            # Sword attack
            if keys[pygame.K_SPACE]:
                attacking = True
                sword_pos = [player_pos[0] + sword_pos_offset[0], player_pos[1] + sword_pos_offset[1]]
                for monster in monsters:
                    monster_rect = pygame.Rect(monster['pos'][0], monster['pos'][1], monster_size, monster_size)
                    if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(monster_rect):
                        monsters.remove(monster)
                        score += 1
                        monsters_slain += 1  # Increment monsters slain count
                        # Reduce sword durability more when hit by a monster
                        sword_durability -= monster_damage
                        if sword_durability <= 0:
                            sword_durability = 0
                        # Transfer sword to player
                        sword_pos = [player_pos[0] + sword_pos_offset[0], player_pos[1] + sword_pos_offset[1]]  # Adjust sword position to follow player

            else:
                attacking = False

            # Regenerate sword durability
            if sword_durability < sword_max_durability:
                sword_durability += sword_regeneration_rate

            # Check if a new monster needs to be spawned
            monster_spawn_timer += 1
            if monster_spawn_timer >= monster_spawn_rate:
                monster_spawn_timer = 0
                spawn_monster()

            # Update monster positions and handle collisions
            game_active = update_monster_positions()

            # Drawing everything
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))
            for monster in monsters:
                pygame.draw.rect(screen, RED, (*monster['pos'], monster_size, monster_size))

            # Display score, health bar, sword health bar, and monsters slain count
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, screen_height - 40))  # Score in bottom left
            draw_health_bar(player_health, 10, 50, 500, 25, "My Health")  # Player health bar
            draw_sword_health_bar(sword_durability, sword_max_durability, screen_width - 510, 50, 500, 25, "Sword Health")  # Sword health bar
            display_monsters_slain(monsters_slain)  # Display monsters slain count

            # Draw the sword if it's spawned
            if attacking:
                screen.blit(sword_img, sword_pos)

            # Draw the healer
            draw_healer()

            pygame.display.flip()

            # Check if game over
            if not game_active:
                game_over_screen(score)

        # Increase difficulty for next level
        wave_count += 1
        player_speed += 1
        player_health += 100

    pygame.quit()

if __name__ == "__main__":
    main()
