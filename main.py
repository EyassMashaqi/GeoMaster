import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


# Load background image
BG_IMAGE_PATH = os.path.join('assets', 'background.png')
if os.path.exists(BG_IMAGE_PATH):
    background_image = pygame.image.load(BG_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    background_image = None

# Try loading a custom font
FONT_PATH = os.path.join('assets', 'YourCustomFont.ttf')
if os.path.exists(FONT_PATH):
    FONT = pygame.font.Font(FONT_PATH, 36)
    FONT_SMALL = pygame.font.Font(FONT_PATH, 28)
else:
    FONT = pygame.font.Font(None, 36)
    FONT_SMALL = pygame.font.Font(None, 28)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
LIGHT_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
GRAY = (50, 50, 50)
YELLOW = (255, 215, 0)

# Panels and highlights have some alpha
PANEL_COLOR = (0, 0, 0, 180)  # Semi-transparent black panel

# Attempt to load sound effects (optional)
CORRECT_SOUND_PATH = os.path.join('assets', 'sounds', 'CorrectAnswer.mp3')
INCORRECT_SOUND_PATH = os.path.join('assets', 'sounds', 'incorrect.mp3')
CLICK_SOUND_PATH = os.path.join('assets', 'sounds', 'Click.mp3')
VICTORY_SOUND_PATH = os.path.join('assets', 'sounds', 'Victory.mp3')
LOSE_SOUND_PATH = os.path.join('assets', 'sounds', 'Sad.mp3')


def load_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        print(f"Sound file not found at {path}")
        return None

correct_sound = load_sound(CORRECT_SOUND_PATH)
incorrect_sound = load_sound(INCORRECT_SOUND_PATH)
click_sound = load_sound(CLICK_SOUND_PATH)
victory_sound = load_sound(VICTORY_SOUND_PATH)
lose_sound = load_sound(LOSE_SOUND_PATH)

# A utility function to safely load images
def load_flag_image(country, size=(100, 60)):
    image_path = os.path.join('assets', 'Flags', f'{country}.png')
    if not os.path.exists(image_path):
        print(f"Warning: Image file not found for {country} at {image_path}. Using fallback.")
        fallback_surface = pygame.Surface(size)
        fallback_surface.fill(RED)
        return fallback_surface
    
    try:
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, size)
        return img
    except (pygame.error, FileNotFoundError) as e:
        print(f"Warning: Could not load image for {country}. Using fallback surface. Error: {e}")
        fallback_surface = pygame.Surface(size)
        fallback_surface.fill(RED)
        return fallback_surface

# Flag to country mapping
country_list = [
    'Palestine', 'Jordan', 'Syria', 'Egypt', 'USA',
    'France', 'Germany', 'Italy', 'Spain', 'UK',
    'India', 'China', 'Japan', 'South Korea', 'Russia',
    'Canada', 'Brazil', 'Mexico', 'Argentina', 'Australia',
    'South Africa', 'Nigeria', 'Kenya', 'Morocco'
]

# Load images for flags
flag_images = {}
for country in country_list:
    flag_images[country] = load_flag_image(country)

# Stage data
stage_data = [
    {
        'flags': ['Palestine', 'Jordan', 'Syria', 'Egypt', 'USA'],
        'capitals': {
            'Palestine': 'Jerusalem',
            'Jordan': 'Amman',
            'Syria': 'Damascus',
            'Egypt': 'Cairo',
            'USA': 'Washington D.C.'
        }
    },
    {
        'flags': ['France', 'Germany', 'Italy', 'Spain', 'UK'],
        'capitals': {
            'France': 'Paris',
            'Germany': 'Berlin',
            'Italy': 'Rome',
            'Spain': 'Madrid',
            'UK': 'London'
        }
    },
    {
        'flags': ['India', 'China', 'Japan', 'South Korea', 'Russia'],
        'capitals': {
            'India': 'New Delhi',
            'China': 'Beijing',
            'Japan': 'Tokyo',
            'South Korea': 'Seoul',
            'Russia': 'Moscow'
        }
    },
    {
        'flags': ['Canada', 'Brazil', 'Mexico', 'Argentina', 'Australia'],
        'capitals': {
            'Canada': 'Ottawa',
            'Brazil': 'Brasília',
            'Mexico': 'Mexico City',
            'Argentina': 'Buenos Aires',
            'Australia': 'Canberra'
        }
    },
    {
        'flags': ['South Africa', 'Egypt', 'Nigeria', 'Kenya', 'Morocco'],
        'capitals': {
            'South Africa': 'Cape Town',
            'Egypt': 'Cairo',
            'Nigeria': 'Abuja',
            'Kenya': 'Nairobi',
            'Morocco': 'Rabat'
        }
    }
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flags and Capitals Game")

# Utility functions
def draw_text(text, font, color, surface, x, y, center=True, shadow=True):
    # Draw text with an optional shadow for better readability
    if shadow:
        shadow_offset = 2
        text_shadow = font.render(text, True, BLACK)
        if center:
            rect = text_shadow.get_rect(center=(x, y))
        else:
            rect = text_shadow.get_rect(topleft=(x, y))
        surface.blit(text_shadow, (rect.x+shadow_offset, rect.y+shadow_offset))

    text_obj = font.render(text, True, color)
    if center:
        text_rect = text_obj.get_rect(center=(x, y))
    else:
        text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(mouse)

    color = active_color if hover else inactive_color
    pygame.draw.rect(surface, color, rect, border_radius=12)

    draw_text(text, FONT, BLACK, surface, x + w // 2, y + h // 2)

    if hover and click[0] == 1 and action:
        if click_sound:
            click_sound.play()
        action()

def draw_health_bar(lives):
    draw_text(f'Lives: {lives}', FONT, WHITE, screen, SCREEN_WIDTH - 200, 40, center=False, shadow=False)

def draw_panel(surface, rect, color=PANEL_COLOR):
    # Draw a semi-transparent panel to highlight content
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill(color)
    surface.blit(panel, rect.topleft)

def fade_in(duration=500):
    # Fade-in effect for a smoother transition
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        alpha = 255 - (elapsed / duration * 255)
        if alpha < 0:
            alpha = 0
        overlay.set_alpha(alpha)
        draw_background()
        screen.blit(overlay, (0,0))
        pygame.display.flip()
        if elapsed >= duration:
            break

def draw_background():
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(DARK_BLUE)

def level(stage_index=0):
    current_stage = stage_data[stage_index]
    flags = current_stage['flags']
    capitals = current_stage['capitals']

    fade_in(700)

    lives = 2
    correct_matches = 0
    total_matches = len(flags)
    selected_flag = None

    # Positioning for flags and capitals
    flag_positions = []
    for idx, country in enumerate(flags):
        x = 100
        y = 150 + idx * 80
        flag_positions.append((country, pygame.Rect(x, y, 100, 60)))

    capital_positions = []
    shuffled_capitals = list(capitals.values())
    random.shuffle(shuffled_capitals)
    for idx, capital in enumerate(shuffled_capitals):
        x = 600
        y = 150 + idx * 80
        text_surf = FONT.render(capital, True, WHITE)
        capital_positions.append((capital, pygame.Rect(x, y, text_surf.get_width(), text_surf.get_height())))

    # List to store matched lines
    matched_lines = []

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a flag was clicked
                for country, rect in flag_positions:
                    if rect.collidepoint(mouse_pos):
                        selected_flag = country

                # Check if a capital was clicked
                for capital, rect in capital_positions:
                    if rect.collidepoint(mouse_pos) and selected_flag:
                        if capitals[selected_flag] == capital:
                            correct_matches += 1
                            if correct_sound:
                                correct_sound.play()

                            # Store the line to draw between the flag and capital
                            flag_rect = next(rect for f, rect in flag_positions if f == selected_flag)
                            capital_rect = next(rect for c, rect in capital_positions if c == capital)
                            matched_lines.append((flag_rect.center, capital_rect.center))

                            # Remove matched items
                            flag_positions = [f for f in flag_positions if f[0] != selected_flag]
                            capital_positions = [c for c in capital_positions if c[0] != capital]
                            selected_flag = None

                            if correct_matches == total_matches:
                                if stage_index < len(stage_data) - 1:
                                    level(stage_index + 1)
                                    return
                                else:
                                    draw_background()
                                    if victory_sound:
                                        victory_sound.play()
                                    draw_text('You Win!', FONT, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                    pygame.display.update()
                                    pygame.time.delay(2000)
                                    running = False
                        else:
                            if incorrect_sound:
                                incorrect_sound.play()
                            lives -= 1
                            selected_flag = None
                            if lives == 0:
                                draw_background()
                                if lose_sound:
                                    lose_sound.play()
                                draw_text('Game Over!', FONT, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                pygame.display.update()
                                pygame.time.delay(2000)
                                running = False

        # Redraw the screen each frame
        draw_background()
        draw_health_bar(lives, max_lives=2)


        draw_text(f'Stage {stage_index + 1}: Match Flags with Capitals', FONT, WHITE, screen, SCREEN_WIDTH // 2, 60)
        draw_text('Click a flag, then click its correct capital.', FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, 100)

        draw_health_bar(lives)

        flag_panel_rect = pygame.Rect(80, 130, 150, (len(flags)*80)+40)
        capital_panel_rect = pygame.Rect(580, 130, 200, (len(shuffled_capitals)*80)+40)
        draw_panel(screen, flag_panel_rect)
        draw_panel(screen, capital_panel_rect)

        for country, rect in flag_positions:
            screen.blit(flag_images[country], rect.topleft)
            if selected_flag == country:
                glow_rect = rect.inflate(20, 20)
                glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surface, (255, 255, 0, 100), glow_surface.get_rect())
                screen.blit(glow_surface, glow_rect.topleft)

        for capital, rect in capital_positions:
            text_surf = FONT.render(capital, True, WHITE)
            capital_bg = pygame.Surface((text_surf.get_width()+20, text_surf.get_height()+10), pygame.SRCALPHA)
            capital_bg.fill((0, 0, 0, 100))
            screen.blit(capital_bg, (rect.x-10, rect.y-5))
            screen.blit(text_surf, rect.topleft)

        # Draw matched lines
        for line in matched_lines:
            pygame.draw.line(screen, (0, 255, 0), line[0], line[1], 4)

        pygame.display.flip()

def draw_health_bar(lives, max_lives=2):
  
    bar_width = 150 
    bar_height = 30  
    bar_x = SCREEN_WIDTH - 240  
    bar_y = 15  

    filled_width = int((lives / max_lives) * bar_width)

    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

    pygame.draw.rect(screen, RED, (bar_x, bar_y, filled_width, bar_height))

    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    draw_text(f'Lives: {lives}/{max_lives}', FONT, WHITE, screen, SCREEN_WIDTH - 220, 17, center=False, shadow=False)

 
def main_menu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_background()
        draw_text('Flags and Capitals Game', FONT, WHITE, screen, SCREEN_WIDTH // 2, 150)

        # Draw start button
        draw_button(screen, 'Start Game', SCREEN_WIDTH // 2 - 100, 300, 200, 50, LIGHT_BLUE, BLUE, lambda: level(0))

        pygame.display.update()

# Run the game
main_menu()