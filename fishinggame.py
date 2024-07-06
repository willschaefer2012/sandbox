import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Game")

# Load images
background_img = pygame.image.load('pond.jpg')
fisherman_img = pygame.image.load('man.jpg')
fish_img = pygame.image.load('fish.jpeg')

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fish_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, SCREEN_WIDTH - 100)
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 100)
        
    def update(self):
        pass

# Fishing line class
class FishingLine(pygame.sprite.Sprite):
    def __init__(self, fisherman):
        super().__init__()
        self.image = pygame.Surface([2, 100])
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = fisherman.rect.centerx - 1
        self.rect.y = fisherman.rect.bottom
        
    def update(self):
        self.rect.y -= 5

# Main game loop
def game_loop():
    running = True
    clock = pygame.time.Clock()
    
    fisherman = pygame.sprite.Sprite()
    fisherman.image = fisherman_img
    fisherman.rect = fisherman.image.get_rect()
    fisherman.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    fishing_line = None
    fishing = False
    caught_fish = None
    score = 0
    
    fish_group = pygame.sprite.Group()
    
    # Add some initial fish
    for _ in range(5):
        fish = Fish()
        fish_group.add(fish)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not fishing:
                    fishing_line = FishingLine(fisherman)
                    fishing = True
        
        if fishing:
            fishing_line.update()
            # Check collision with fish
            fish_collisions = pygame.sprite.spritecollide(fishing_line, fish_group, True)
            if fish_collisions:
                caught_fish = fish_collisions[0]
                score += 1
                fishing = False
                fishing_line = None
                fish = Fish()
                fish_group.add(fish)
        
        # Clear screen
        screen.blit(background_img, (0, 0))
        
        # Draw fisherman
        screen.blit(fisherman.image, fisherman.rect)
        
        # Draw fishing line
        if fishing_line:
            pygame.draw.line(screen, BROWN, (fisherman.rect.centerx, fisherman.rect.bottom), (fishing_line.rect.centerx, fishing_line.rect.y), 2)
        
        # Draw fish
        fish_group.update()
        fish_group.draw(screen)
        
        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game_loop()
