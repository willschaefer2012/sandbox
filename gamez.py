import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Home Screen Example")

# Load assets
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 40)

# Button texts
start_button_text = button_font.render('Start', True, (0, 0, 0))
settings_button_text = button_font.render('Settings', True, (0, 0, 0))
red_button_text = button_font.render('Red', True, (0, 0, 0))
green_button_text = button_font.render('Green', True, (0, 0, 0))
blue_button_text = button_font.render('Blue', True, (0, 0, 0))

# Unicode arrow character for back arrow
back_arrow = u'\u25C4'  # Black left-pointing triangle
back_button_text = button_font.render(back_arrow, True, (0, 0, 0))

# Button settings
button_color_default = (0, 255, 0)
button_hover_color = (0, 200, 0)
button_border_color = (255, 255, 255)
button_border_thickness_default = 5
button_border_thickness_hover = 10

start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 120, 200, 60)
settings_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 40, 200, 60)

red_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 140, 200, 60)
green_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 60, 200, 60)
blue_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 200, 60)
back_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)

# Initial background color
background_color = (0, 0, 0)

# Function to draw a rounded rectangle button with a border
def draw_rounded_button(screen, rect, color, border_color, border_thickness, text, corner_radius=20):
    pygame.draw.rect(screen, border_color, rect, border_radius=corner_radius, width=border_thickness)
    inner_rect = rect.inflate(-border_thickness * 2, -border_thickness * 2)
    pygame.draw.rect(screen, color, inner_rect, border_radius=corner_radius)
    screen.blit(text, (inner_rect.x + (inner_rect.width - text.get_width()) // 2, inner_rect.y + (inner_rect.height - text.get_height()) // 2))

# Function to handle the home screen
def home_screen():
    global running, background_color
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background_color)

        # Check if the mouse is over the start button
        if start_button_rect.collidepoint(mouse_pos):
            start_button_color = button_hover_color
            start_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                print("Game Started")
                running = False
        else:
            start_button_color = button_color_default
            start_button_border_thickness = button_border_thickness_default

        # Check if the mouse is over the settings button
        if settings_button_rect.collidepoint(mouse_pos):
            settings_button_color = button_hover_color
            settings_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                settings_screen()
        else:
            settings_button_color = button_color_default
            settings_button_border_thickness = button_border_thickness_default

        draw_rounded_button(screen, start_button_rect, start_button_color, button_border_color, start_button_border_thickness, start_button_text)
        draw_rounded_button(screen, settings_button_rect, settings_button_color, button_border_color, settings_button_border_thickness, settings_button_text)

        pygame.display.flip()

# Function to handle the settings screen
def settings_screen():
    global running, background_color
    in_settings = True
    while in_settings:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background_color)

        # Check for color selection
        if red_button_rect.collidepoint(mouse_pos):
            red_button_color = button_hover_color
            red_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                background_color = (255, 0, 0)
        else:
            red_button_color = button_color_default
            red_button_border_thickness = button_border_thickness_default

        if green_button_rect.collidepoint(mouse_pos):
            green_button_color = button_hover_color
            green_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                background_color = (0, 255, 0)
        else:
            green_button_color = button_color_default
            green_button_border_thickness = button_border_thickness_default

        if blue_button_rect.collidepoint(mouse_pos):
            blue_button_color = button_hover_color
            blue_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                background_color = (0, 0, 255)
        else:
            blue_button_color = button_color_default
            blue_button_border_thickness = button_border_thickness_default

        # Check for back button
        if back_button_rect.collidepoint(mouse_pos):
            back_button_color = button_hover_color
            back_button_border_thickness = button_border_thickness_hover
            if mouse_pressed[0]:  # Left mouse button is pressed
                in_settings = False
        else:
            back_button_color = button_color_default
            back_button_border_thickness = button_border_thickness_default

        draw_rounded_button(screen, red_button_rect, red_button_color, button_border_color, red_button_border_thickness, red_button_text)
        draw_rounded_button(screen, green_button_rect, green_button_color, button_border_color, green_button_border_thickness, green_button_text)
        draw_rounded_button(screen, blue_button_rect, blue_button_color, button_border_color, blue_button_border_thickness, blue_button_text)
        draw_rounded_button(screen, back_button_rect, back_button_color, button_border_color, back_button_border_thickness, back_button_text)

        pygame.display.flip()

# Main loop
running = True
home_screen()

# Game loop can go here after the home screen
# ...

pygame.quit()
