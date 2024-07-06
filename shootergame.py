import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Player
player_width, player_height = 50, 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Bullet
bullet_width, bullet_height = 5, 10
bullet_speed = 7
bullets = []

# Enemy
enemy_width, enemy_height = 50, 50
enemy_speed = 3
enemies = []

# Score
score = 0

# Game loop control
running = True
clock = pygame.time.Clock()

class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color, font, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.font = font
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.action:
                self.action()

def start_game():
    global running
    global player_x, player_y, bullets, enemies, score
    
    # Reset game variables
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    bullets = []
    enemies = []
    score = 0
    
    def draw_player(x, y):
        pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

    def draw_bullet(x, y):
        pygame.draw.rect(screen, RED, (x, y, bullet_width, bullet_height))

    def draw_enemy(x, y):
        pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

        screen.fill(BLACK)

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.randint(1, 20) == 1:
            enemies.append([random.randint(0, WIDTH - enemy_width), 0])

        # Move enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score -= 1  # Lose a point if an enemy reaches the bottom

        # Check for collisions
        bullets_to_remove = []
        enemies_to_remove = []
        
        for enemy in enemies:
            for bullet in bullets:
                if (bullet[0] >= enemy[0] and bullet[0] <= enemy[0] + enemy_width and
                        bullet[1] >= enemy[1] and bullet[1] <= enemy[1] + enemy_height):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    score += 1
        
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        # Draw player, bullets, and enemies
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])

        show_score(score)

        pygame.display.flip()
        clock.tick(60)

def shop():
    print("Shop clicked")

def settings():
    print("Settings clicked")

def main_menu():
    start_button = Button("Start", WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50, GRAY, DARK_GRAY, small_font, start_game)
    shop_button = Button("Shop", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GRAY, DARK_GRAY, small_font, shop)
    settings_button = Button("Settings", WIDTH // 2 - 100, HEIGHT // 2 + 125, 200, 50, GRAY, DARK_GRAY, small_font, settings)
    
    buttons = [start_button, shop_button, settings_button]
    
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render("Shooter Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for button in buttons:
                button.handle_event(event)

        clock.tick(60)

# Main game loop
main_menu()
pygame.quit()
