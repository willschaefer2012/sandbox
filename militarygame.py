import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Simple Military Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green_color = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Font for name tag and death zone text
font = pygame.font.SysFont("monospace", 15)
blood_font = pygame.font.Font(None, 36)

# Player properties
player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 10

# Gun properties
gun_width = 5
gun_height = 15

# Bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = 15
bullets = []

# Enemy properties
enemy_size = 50
enemy_speed = 5  # Reduced enemy speed
enemies = [[random.randint(0, screen_width - enemy_size), 0] for _ in range(5)]

# Dog properties
dog_size = 20
dog_pos = list(player_pos)
dog_active = False
dog_speed = 7
dog_hits = 0  # Counter for the number of enemies REX has hit

# Giant barrier (Death Zone) properties
death_zone_color = (255, 0, 0)
death_zone_active = False
death_zone_pos = [0, screen_height - 50]  # Position and size of the death zone

# Damage value for the death zone
death_zone_damage = 50

# Counter for remaining kills needed to activate phases
kills_needed_for_death_zone = 10
kills_needed_after_death_zone = 25
total_enemies_defeated = 0

# Timer properties
timer_font = pygame.font.SysFont("monospace", 20)
timer_duration = 10  # 10 seconds timer
timer_start = None
show_timer = False

# Green ring (Death Protector) properties
green_ring_color = (0, 255, 0)
green_ring_radius = 100
green_ring_active = False
green_ring_pos = player_pos.copy()  # Initial position at player's position

# Game loop
game_over = False
clock = pygame.time.Clock()

def detect_collision(obj1_pos, obj2_pos, obj1_size, obj2_size):
    o1_x, o1_y = obj1_pos
    o2_x, o2_y = obj2_pos
    
    if (o2_x >= o1_x and o2_x < (o1_x + obj1_size)) or (o1_x >= o2_x and o1_x < (o2_x + obj2_size)):
        if (o2_y >= o1_y and o2_y < (o1_y + obj1_size)) or (o1_y >= o2_y and o1_y < (o2_y + obj2_size)):
            return True
    return False

def update_bullets(bullets):
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets[:] = [bullet for bullet in bullets if bullet[1] > 0]

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, green_color, (bullet[0], bullet[1], bullet_width, bullet_height))

def update_enemies(enemies):
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemy[1] = 0
            enemy[0] = random.randint(0, screen_width - enemy_size)

def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, red, (enemy[0], enemy[1], enemy_size, enemy_size))

def find_nearest_enemy(dog_pos, enemies):
    nearest_enemy = None
    min_distance = float('inf')
    for enemy in enemies:
        distance = math.sqrt((enemy[0] - dog_pos[0])**2 + (enemy[1] - dog_pos[1])**2)
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    return nearest_enemy

def move_dog_towards_enemy(dog_pos, enemy_pos, dog_speed):
    if not enemy_pos:
        return
    dx = enemy_pos[0] - dog_pos[0]
    dy = enemy_pos[1] - dog_pos[1]
    dist = math.sqrt(dx**2 + dy**2)
    if dist != 0:
        dog_pos[0] += int(dog_speed * dx / dist)
        dog_pos[1] += int(dog_speed * dy / dist)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    
    # Movement controls
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
        player_pos[1] += player_speed
    
    if keys[pygame.K_SPACE]:
        bullets.append([player_pos[0] + player_size // 2 - bullet_width // 2, player_pos[1]])
    if keys[pygame.K_d] and not dog_active:
        dog_active = True
        dog_pos = list(player_pos)

    screen.fill(black)

    update_bullets(bullets)
    update_enemies(enemies)

    for enemy in enemies[:]:
        if detect_collision(player_pos, enemy, player_size, enemy_size):
            game_over = True
        for bullet in bullets[:]:
            if detect_collision(bullet, enemy, bullet_width, enemy_size):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    enemies.append([random.randint(0, screen_width - enemy_size), 0])
                    total_enemies_defeated += 1

    if total_enemies_defeated >= kills_needed_for_death_zone and not death_zone_active:
        death_zone_active = True
        death_zone_pos = [0, screen_height - 50]  # Adjust death zone position and size
        timer_start = pygame.time.get_ticks()  # Start the timer

    if death_zone_active:
        # Draw Death Zone text
        death_zone_text = blood_font.render("Death Zone", True, red)
        screen.blit(death_zone_text, (screen_width // 2 - death_zone_text.get_width() // 2, screen_height // 2 - death_zone_text.get_height() // 2))
        # Draw Death Zone barrier
        pygame.draw.rect(screen, death_zone_color, (death_zone_pos[0], death_zone_pos[1], screen_width, 50))  # Adjust dimensions here

        # Check collisions with the death zone
        for enemy in enemies[:]:
            if detect_collision((death_zone_pos[0], death_zone_pos[1]), enemy, screen_width, 50):
                enemies.remove(enemy)
                total_enemies_defeated += 1  # Increase the defeated enemies count

        # Timer logic
        if timer_start is not None:
            elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000  # Convert milliseconds to seconds
            if elapsed_time <= timer_duration:
                timer_text = timer_font.render(f"Timer: {timer_duration - elapsed_time}", True, red)  # Timer text in red color
                timer_text_rect = timer_text.get_rect()
                timer_text_rect.topright = (screen_width - 10, 10)
                screen.blit(timer_text, timer_text_rect)
            else:
                # Timer expired, deactivate Death Zone
                death_zone_active = False
                timer_start = None

    if not death_zone_active and total_enemies_defeated >= kills_needed_after_death_zone:
        # Activate green ring (Death Protector)
        green_ring_active = True
        green_ring_pos = player_pos.copy()
        total_enemies_defeated = 0  # Reset total enemies defeated for the green ring phase
        kills_needed_for_death_zone = 0  # Set to zero so it doesn't re-activate death zone logic

    if green_ring_active:
        # Update green ring position to follow player
        green_ring_pos = player_pos.copy()
        
        pygame.draw.circle(screen, green_color, (green_ring_pos[0] + player_size // 2, green_ring_pos[1] + player_size // 2), green_ring_radius)

        # Check collisions with the green ring
        for enemy in enemies[:]:
            enemy_center = (enemy[0] + enemy_size // 2, enemy[1] + enemy_size // 2)
            distance = math.sqrt((enemy_center[0] - (green_ring_pos[0] + player_size // 2))**2 + (enemy_center[1] - (green_ring_pos[1] + player_size // 2))**2)
            if distance <= green_ring_radius:
                enemies.remove(enemy)
                total_enemies_defeated += 1  # Increase the defeated enemies count

        # Draw counter for remaining kills needed for green ring
        if kills_needed_after_death_zone > total_enemies_defeated:
            green_ring_text = font.render(f"Kills left for Green Ring: {max(0, kills_needed_after_death_zone - total_enemies_defeated)}", True, green_color)
            green_ring_text_rect = green_ring_text.get_rect()
            green_ring_text_rect.topright = (screen_width - 10, 30)
            screen.blit(green_ring_text, green_ring_text_rect)
        else:
            green_ring_active = False  # Green ring phase ends when all kills are achieved

    if dog_active:
        nearest_enemy = find_nearest_enemy(dog_pos, enemies)
        if nearest_enemy:
            move_dog_towards_enemy(dog_pos, nearest_enemy, dog_speed)
            if detect_collision(dog_pos, nearest_enemy, dog_size, enemy_size):
                if nearest_enemy in enemies:
                    enemies.remove(nearest_enemy)
                    enemies.append([random.randint(0, screen_width - enemy_size), 0])
                    dog_hits += 1
                    if dog_hits >= 7:
                        dog_active = False

        pygame.draw.rect(screen, blue, (dog_pos[0] + player_size // 2 - dog_size // 2, dog_pos[1], dog_size, dog_size))
        
        # Render and draw the name tag "REX"
        name_tag = font.render("REX", True, white)
        screen.blit(name_tag, (dog_pos[0] + player_size // 2 - dog_size // 2, dog_pos[1] - 20))

    draw_enemies(enemies)
    draw_bullets(bullets)
    
    pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size))
    
    # Draw gun
    gun_x = player_pos[0] + player_size // 2 - gun_width // 2
    gun_y = player_pos[1] - gun_height
    pygame.draw.rect(screen, white, (gun_x, gun_y, gun_width, gun_height))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
