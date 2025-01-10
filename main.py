import pygame
import sys
import random
import os
import pygal
from itertools import permutations



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
    FONT_SMALL = pygame.font.Font(None, 28)
    FONT = pygame.font.Font(None, 36)
    FONT_MEDIUM = pygame.font.Font(None, 48)
    FONT_LARGE = pygame.font.Font(None, 100)

CAPITALS_MUSIC_PATH = os.path.join('assets', 'sounds', 'capitals.mp3')
FLAGS_MUSIC_PATH = os.path.join('assets', 'sounds', 'flags.mp3')
MONUMENTS_MUSIC_PATH = os.path.join('assets', 'sounds', 'monument.mp3')
MENU_MUSIC_PATH = os.path.join('assets', 'sounds', 'main.mp3')

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
EMERALD_GREEN = (50, 200, 120)
HOVER_EMERALD_GREEN = (60, 220, 140)
LIGHT_CORAL = (240, 128, 128)
ORANGE = (255, 165, 0)
LIME_GREEN = (50, 205, 50)
DEEP_PINK = (255, 20, 147)
DARK_NAVY = (0, 0, 80)


def change_background_music(music_path):
    if os.path.exists(music_path):
        pygame.mixer.music.stop()  # Stop current music
        pygame.mixer.music.load(music_path)  # Load the new track
        pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    else:
        print(f"Warning: Music file not found at {music_path}")

# Load flag images
def load_flag_image(name, size=(180, 120)):
    path = os.path.join('assets', 'Flags', f'{name}.png')
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    else:
        # Placeholder for missing flags
        img = pygame.Surface(size)
        img.fill(GRAY)
        return img

# Generate flag variations

def run_sequential_game():
    total_score = 0
    max_score = 0

    # Define the levels in sequence
    levels = [
        ("Country Capitals", lambda: level(0)),
        ("Flag Guessing", flag_guessing_game),
        ("Monument Quiz", monument_question_level)
    ]

    for level_name, level_func in levels:
        # Display level start message
        draw_background()
        draw_text_with_shadow(f"Starting {level_name}", FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(2000)

        # Run the level and get the score
        level_score, level_max_score = level_func()
        total_score += level_score
        max_score += level_max_score

        # Show interim score
        draw_background()
        draw_text_with_shadow(
            f"{level_name} Complete! Score: {level_score}/{level_max_score}",
            FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        pygame.display.update()
        pygame.time.wait(3000)

    # Final score display
    show_final_score(total_score, max_score)

    def show_final_score(total_score, max_score):
        draw_gradient_background(screen, LIGHT_BLUE, DARK_BLUE)
        box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
        pygame.draw.rect(screen, YELLOW if total_score > max_score // 2 else RED, box_rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, box_rect, 5, border_radius=15)
    
        message = "Victory!" if total_score > max_score // 2 else "Game Over!"
        draw_text(message, FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text(f"Total Score: {total_score}/{max_score}", FONT_SMALL, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        pygame.display.update()
        pygame.time.wait(5000)



def generate_variations(country, size=(180, 120), bg_color=(255, 255, 255)):
    # Load the correct flag image
    correct_flag = load_flag_image(country, size)
    incorrect_flags = []

    # Analyze flag structure
    regions = [
        pygame.Rect(0, 0, size[0] // 3, size[1]),        # Left section
        pygame.Rect(size[0] // 3, 0, size[0] // 3, size[1]),  # Middle section
        pygame.Rect(2 * size[0] // 3, 0, size[0] // 3, size[1])  # Right section
    ]

    # Extract and copy the regions
    segments = [correct_flag.subsurface(region).copy() for region in regions]

    # Generate all unique permutations of the regions
    all_permutations = list(permutations(segments))
    random.shuffle(all_permutations)  # Randomize the order of permutations

    # Select two unique permutations that are not the same as the correct order
    incorrect_variations = [perm for perm in all_permutations if perm != tuple(segments)]
    selected_variations = incorrect_variations[:2]

    # Create flag variations based on the selected permutations
    for variation_order in selected_variations:
        variation = pygame.Surface(size)
        variation.fill(bg_color)  # Set background color
        for i, segment in enumerate(variation_order):
            variation.blit(segment, (i * (size[0] // 3), 0))  # Place segments
        incorrect_flags.append(variation)

    return correct_flag, incorrect_flags
# Draw the GUI
def draw_gui(country, options, option_positions, message=None):
    # Fill the screen background
    screen.fill(WHITE)

    # Display the question
    font = pygame.font.Font(None, 48)
    question_text = font.render(f"What is the correct flag for {country}?", True, BLACK)
    screen.blit(question_text, (400 - question_text.get_width() // 2, 50))

    # Display options in boxes
    for i, option in enumerate(options):
        x, y = option_positions[i]
        rect = pygame.Rect(x - 10, y - 10, 200, 140)  # Box around the flag
        pygame.draw.rect(screen, BLACK, rect, 2)
        screen.blit(option, (x, y))

    # Display message if any
    if message:
        message_font = pygame.font.Font(None, 36)
        message_text = message_font.render(message, True, RED if "Incorrect" in message else BLUE)
        screen.blit(message_text, (400 - message_text.get_width() // 2, 500))

    pygame.display.flip()
    
        
    
    
def flag_guessing_game():
    change_background_music(FLAGS_MUSIC_PATH)
    print("Starting Flag Guessing Game")

    # Load flags background
    FLAGS_BACKGROUND_PATH = os.path.join('assets', 'flags_background.png')
    flags_background = pygame.image.load(FLAGS_BACKGROUND_PATH)
    flags_background = pygame.transform.scale(flags_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    rounds = 5  # Number of rounds
    score = 0  # Track correct guesses

    for round_number in range(1, rounds + 1):
        country = random.choice(country_list)  # Randomly select a country
        correct_flag = load_flag_image(country)  # Load correct flag image

        # Select two incorrect flags (ensure they are different from the correct one)
        incorrect_countries = [c for c in country_list if c != country]
        incorrect_flags = random.sample(incorrect_countries, 2)
        incorrect_images = [load_flag_image(inc) for inc in incorrect_flags]

        # Combine correct flag with incorrect flags
        options = [correct_flag] + incorrect_images
        random.shuffle(options)
        option_positions = [(200, 300), (400, 300), (600, 300)]  # Positioned in one row

        # Determine the index of the correct flag
        correct_index = options.index(correct_flag)
        running = True
        message = None

        while running:
            # Draw the flags background
            screen.blit(flags_background, (0, 0))

            # Draw background panels for question and options
            draw_panel(screen, pygame.Rect(100, 50, 700, 100), (0, 0, 0, 150))  # Question panel
            draw_panel(screen, pygame.Rect(100, 250, 700, 200), (0, 0, 0, 100))  # Options panel

            # Display question and score
            draw_text(f"Round {round_number} / {rounds}", FONT, WHITE, screen, 150, 50, center=False)
            draw_text(f"Score: {score}", FONT, WHITE, screen, SCREEN_WIDTH - 200, 50, center=False)
            draw_text(f"What is the flag of {country}?", FONT, YELLOW, screen, SCREEN_WIDTH // 2, 100)

            # Draw the options with hover effect
            for i, option in enumerate(options):
                x, y = option_positions[i]
                rect = pygame.Rect(x, y, 180, 120)

                # Add hover effect with glow
                if rect.collidepoint(pygame.mouse.get_pos()):
                    glow_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (255, 255, 0, 120), glow_surface.get_rect(), border_radius=15)
                    screen.blit(glow_surface, rect.topleft)
                else:
                    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=15)

                # Center the flag inside the border
                flag_rect = option.get_rect(center=rect.center)
                screen.blit(option, flag_rect.topleft)

            # Display feedback message
            if message:
                draw_text(message, FONT, RED if "Incorrect" in message else GREEN, screen, SCREEN_WIDTH // 2, 500)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, (x, y) in enumerate(option_positions):
                        rect = pygame.Rect(x, y, 180, 120)
                        if rect.collidepoint(mouse_pos):
                            if i == correct_index:
                                message = "Correct!"
                                score += 1
                                highlight_box(screen, rect, GREEN)
                                if correct_sound:
                                    correct_sound.play()
                            else:
                                message = f"Incorrect! The correct answer was: {country}"
                                highlight_box(screen, rect, RED)
                                if incorrect_sound:
                                    incorrect_sound.play()
                            pygame.time.wait(1500)
                            running = False

    # End of game summary
    show_end_screen(score, rounds)






# Function to show victory or loss screen
def show_end_screen(score, rounds):
    draw_gradient_background(screen, LIGHT_BLUE, DARK_BLUE)
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
    pygame.draw.rect(screen, YELLOW if score > rounds // 2 else RED, box_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, box_rect, 5, border_radius=15)

    # Victory or Loss Message
    if score > rounds // 2:
        message = "Victory! Well Done!"
        if victory_sound:
            victory_sound.play()
    else:
        message = "Game Over! Better Luck Next Time!"
        if lose_sound:
            lose_sound.play()

    draw_text(message, FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
    draw_text(f"Final Score: {score}/{rounds}", FONT_SMALL, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
    pygame.display.update()
    pygame.time.wait(4000)



# Panels and highlights have some alpha
PANEL_COLOR = (0, 0, 0, 180)  # Semi-transparent black panel

# Attempt to load sound effects (optional)
CORRECT_SOUND_PATH = os.path.join('assets', 'sounds', 'CorrectAnswer.mp3')
INCORRECT_SOUND_PATH = os.path.join('assets', 'sounds', 'incorrect.mp3')
CLICK_SOUND_PATH = os.path.join('assets', 'sounds', 'Click.mp3')
VICTORY_SOUND_PATH = os.path.join('assets', 'sounds', 'Victory.mp3')
LOSE_SOUND_PATH = os.path.join('assets', 'sounds', 'Sad2.mp3')


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
draw_sound = None  # Define draw_sound to avoid undefined error

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

stage_data.append({
    'monuments': {
        'Palestine': 'Dome of the Rock',
        'France': 'Eiffel Tower',
        'India': 'Taj Mahal',
        'USA': 'Statue of Liberty',
        'Egypt': 'Great Pyramid of Giza',
        'China': 'Great Wall of China',
        'Italy': 'Colosseum',
        'UK': 'Big Ben',
        'Brazil': 'Christ the Redeemer',
        'Australia': 'Sydney Opera House'
    }
})

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
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        if elapsed >= duration:
            break

def fade_out(duration=500):
    # Fade-out effect for a smoother transition
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    start_time = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start_time
        alpha = int((elapsed / duration) * 255)
        if alpha > 255:
            alpha = 255
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        if elapsed >= duration:
            break

def draw_background():
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(DARK_BLUE)

def level(stage_index=0, total_score=0):
    level_bg = os.path.join('assets', 'background.png')
    if os.path.exists(level_bg):
        bg_image = pygame.image.load(level_bg)
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
    change_background_music(CAPITALS_MUSIC_PATH)
    if 'flags' not in stage_data[stage_index]:
        print(f"Error: Stage {stage_index} does not contain 'flags'.")
        return total_score

    current_stage = stage_data[stage_index]
    flags = current_stage['flags']
    capitals = current_stage['capitals']

    fade_in(700)

    lives = 2
    correct_matches = 0
    total_matches = len(flags)
    selected_flag = None

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

    matched_lines = []

    def draw_gradient_line(surface, start_pos, end_pos, color_start, color_end, width):
        x1, y1 = start_pos
        x2, y2 = end_pos
        for i in range(0, 101, 2):  # Adjust step for smoother gradient
            alpha = i / 100
            x = x1 + (x2 - x1) * alpha
            y = y1 + (y2 - y1) * alpha
            color = (
                int(color_start[0] + (color_end[0] - color_start[0]) * alpha),
                int(color_start[1] + (color_end[1] - color_start[1]) * alpha),
                int(color_start[2] + (color_end[2] - color_start[2]) * alpha),
            )
            pygame.draw.circle(surface, color, (int(x), int(y)), width // 2)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for country, rect in flag_positions:
                    if rect.collidepoint(mouse_pos):
                        selected_flag = country

                for capital, rect in capital_positions:
                    if rect.collidepoint(mouse_pos) and selected_flag:
                        if capitals[selected_flag] == capital:
                            correct_matches += 1
                            total_score += 1
                            if correct_sound:
                                correct_sound.play()

                            flag_rect = next(rect for f, rect in flag_positions if f == selected_flag)
                            capital_rect = next(rect for c, rect in capital_positions if c == capital)
                            matched_lines.append((flag_rect.center, capital_rect.center))

                            flag_positions = [f for f in flag_positions if f[0] != selected_flag]
                            capital_positions = [c for c in capital_positions if c[0] != capital]
                            selected_flag = None

                            if correct_matches == total_matches:
                                fade_out(700)
                                if stage_index < len(stage_data) - 1:
                                    return level(stage_index + 1, total_score)
                                else:
                                    # Final victory message
                                    draw_background()
                                    draw_text("Congratulations! You completed the game!", FONT, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
                                    draw_text(f"Final Score: {total_score}", FONT_SMALL, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
                                    if victory_sound:
                                        victory_sound.play()
                                    pygame.display.update()
                                    pygame.time.delay(5000)
                                    running = False
                                    return total_score
                        else:
                            if incorrect_sound:
                                incorrect_sound.play()
                            lives -= 1
                            selected_flag = None
                            if lives == 0:
                                draw_background()
                                draw_text("Game Over!", FONT, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                draw_text(f"Total Score: {total_score}", FONT_SMALL, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
                                if lose_sound:
                                    lose_sound.play()
                                pygame.display.update()
                                pygame.time.delay(5000)
                                running = False
                                return total_score

        # draw_background()
        draw_health_bar(lives)

        draw_text(f"Stage: {stage_index + 1} | Correct Matches: {correct_matches} / {total_matches}", FONT, WHITE, screen, SCREEN_WIDTH // 2, 40)
        draw_text(f"Score: {total_score}", FONT, WHITE, screen, 50, 40, center=False)

        draw_text("Click a flag, then click its correct capital.", FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, 100)

        draw_panel(screen, pygame.Rect(80, 130, 150, (len(flags) * 80) + 40))
        draw_panel(screen, pygame.Rect(580, 130, 250, (len(shuffled_capitals) * 80) + 40))

        for country, rect in flag_positions:
            screen.blit(flag_images[country], rect.topleft)
            if selected_flag == country:
                glow_rect = rect.inflate(10, 10)  # Bigger glow
                glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)

                # Adjusted glow to center it over the flag
                for alpha, size in zip([50, 100, 150, 200], [40, 30, 20, 10]):
                    glow_layer = rect.inflate(size, size)
                    offset_x = (glow_layer.width - rect.width) // 2
                    offset_y = (glow_layer.height - rect.height) // 2
                    pygame.draw.ellipse(
                        glow_surface,
                        (255, 255, 0, alpha),
                        glow_surface.get_rect().move(-offset_x, -offset_y)
                    )

                screen.blit(glow_surface, glow_rect.topleft)

        for capital, rect in capital_positions:
            text_surf = FONT.render(capital, True, WHITE)
            capital_bg = pygame.Surface((text_surf.get_width() + 20, text_surf.get_height() + 10), pygame.SRCALPHA)
            capital_bg.fill((0, 0, 0, 100))
            screen.blit(capital_bg, (rect.x - 10, rect.y - 5))
            screen.blit(text_surf, rect.topleft)

        for line in matched_lines:
            draw_gradient_line(screen, line[0], line[1], (0, 255, 0), (0, 128, 0), 4)

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



def monument_question_level(total_score=0):
    # Load the custom background image
    bg_image_path = os.path.join('assets', 'monument_background.webp')
    if os.path.exists(bg_image_path):
        bg_image = pygame.image.load(bg_image_path)
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        print(f"Warning: Background image not found at {bg_image_path}. Using solid color.")
        bg_image = None

    change_background_music(MONUMENTS_MUSIC_PATH)
    fade_in(700)

    # Extract monuments data
    current_stage = stage_data[-1]  # Assuming monuments are the last stage
    monuments = current_stage.get('monuments', {})
    countries = list(monuments.keys())
    all_monuments = list(monuments.values())

    rounds = 5  # Number of questions
    score = 0  # Track correct answers in this level

    for round_number in range(1, rounds + 1):
        # Select a random country and its correct monument
        country = random.choice(countries)
        correct_monument = monuments[country]

        # Generate options (1 correct + 3 incorrect)
        incorrect_monuments = random.sample(
            [mon for mon in all_monuments if mon != correct_monument], 3
        )
        options = incorrect_monuments + [correct_monument]
        random.shuffle(options)

        # Display question
        running = True
        selected_option = None
        message = None

        while running:
            # Draw the background
            if bg_image:
                screen.blit(bg_image, (0, 0))
            else:
                screen.fill(DARK_BLUE)

            # Display round and score
            draw_panel(screen, pygame.Rect(10, 10, SCREEN_WIDTH - 20, 60), (0, 0, 0, 120))
            draw_text(f"Round {round_number} / {rounds}", FONT, WHITE, screen, 50, 30, center=False)
            draw_text(f"Score: {score}", FONT, WHITE, screen, SCREEN_WIDTH - 150, 30, center=False)

            # Display the question with larger text and slightly lower position
            draw_text(f"Which monument is in {country}?", FONT_MEDIUM, YELLOW, screen, SCREEN_WIDTH // 2, 140)

            # Calculate button layout for 2 rows and 2 columns (centered)
            option_positions = []
            total_button_width = 2 * 300 + 50  # 300px button width, 50px gap between columns
            total_button_height = 2 * 60 + 40  # 60px button height, 40px gap between rows
            start_x = (SCREEN_WIDTH - total_button_width) // 2
            start_y = (SCREEN_HEIGHT - total_button_height) // 2 + 70  # Center vertically with offset

            button_width = 300
            button_height = 60
            gap_x = 50  # Horizontal gap between buttons
            gap_y = 40  # Vertical gap between buttons

            for i, option in enumerate(options):
                row = i // 2  # Calculate row index (0 or 1)
                col = i % 2   # Calculate column index (0 or 1)
                x = start_x + col * (button_width + gap_x)
                y = start_y + row * (button_height + gap_y)
                rect = pygame.Rect(x, y, button_width, button_height)
                option_positions.append((option, rect))

                # Detect hover
                if rect.collidepoint(pygame.mouse.get_pos()):
                    # Hover effect with gradient
                    draw_gradient_box(screen, rect, (255, 255, 100), (255, 215, 0), border_radius=15)
                else:
                    # Normal button
                    draw_gradient_box(screen, rect, (135, 206, 250), (30, 144, 255), border_radius=15)

                draw_text(option, FONT, WHITE, screen, rect.centerx, rect.centery)

            # Display feedback message
            if message:
                draw_text(message, FONT, RED if "Incorrect" in message else GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, (option, rect) in enumerate(option_positions):
                        if rect.collidepoint(mouse_pos):
                            selected_option = option
                            if selected_option == correct_monument:
                                score += 1
                                total_score += 1  # Increment total score
                                message = "Correct!"
                                highlight_box(screen, rect, GREEN)
                                if correct_sound:
                                    correct_sound.play()
                            else:
                                message = f"Incorrect! The correct answer was: {correct_monument}"
                                highlight_box(screen, rect, RED)
                                if incorrect_sound:
                                    incorrect_sound.play()
                            pygame.time.wait(1500)
                            running = False

    # End of level summary
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(DARK_BLUE)

    if score >= rounds // 2:
        message = "Victory! Well Done!"
        if victory_sound:
            victory_sound.play()
    else:
        message = "Game Over! Better Luck Next Time!"
        if lose_sound:
            lose_sound.play()

    draw_text(message, FONT, GREEN if score >= rounds // 2 else RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
    draw_text(f"Level Score: {score}/{rounds} | Total Score: {total_score}", FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.display.update()
    pygame.time.wait(5000)

    return total_score



# Function to draw gradient box
def draw_gradient_box(surface, rect, color1, color2, border_radius=0):
    gradient_surface = pygame.Surface((rect.width, rect.height))
    for y in range(rect.height):
        ratio = y / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(gradient_surface, (r, g, b), (0, y), (rect.width, y))
    gradient_surface = pygame.transform.smoothscale(gradient_surface, (rect.width, rect.height))
    surface.blit(gradient_surface, rect.topleft)

# Function to highlight selected box
def highlight_box(surface, rect, color):
    highlight_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(highlight_surface, (*color, 150), highlight_surface.get_rect(), border_radius=10)
    surface.blit(highlight_surface, rect.topleft)


def main_menu():
    # Load the background image
    image_path= os.path.join('assets', 'mainMenu_background.webp')
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    change_background_music(MENU_MUSIC_PATH)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw the game title with shadow
        draw_text_with_shadow('GeoMaster', FONT_LARGE, WHITE, screen, SCREEN_WIDTH // 2, 100, shadow_offset=6)

        # Draw buttons
        draw_button(screen, 'Country Capitals', SCREEN_WIDTH // 2 - 100, 250, 250, 50, EMERALD_GREEN, HOVER_EMERALD_GREEN, lambda: level(0))
        draw_button(screen, 'Flag Guessing', SCREEN_WIDTH // 2 - 100, 320, 250, 50, EMERALD_GREEN, HOVER_EMERALD_GREEN, flag_guessing_game)
        draw_button(screen, 'Monument Quiz', SCREEN_WIDTH // 2 - 100, 390, 250, 50,EMERALD_GREEN, HOVER_EMERALD_GREEN, monument_question_level)

        pygame.display.update()


# Function to draw gradient background
def draw_gradient_background(surface, color1, color2):
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

# Function to draw text with shadow
def draw_text_with_shadow(text, font, color, surface, x, y, shadow_color=BLACK, shadow_offset=3):
    # Draw shadow
    shadow_text = font.render(text, True, shadow_color)
    shadow_rect = shadow_text.get_rect(center=(x + shadow_offset, y + shadow_offset))
    surface.blit(shadow_text, shadow_rect)

    # Draw main text
    main_text = font.render(text, True, color)
    main_rect = main_text.get_rect(center=(x, y))
    surface.blit(main_text, main_rect)

# Updated button function with hover effect
def draw_button(surface, text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(mouse)

    color = active_color if hover else inactive_color

    # Draw button with rounded corners
    pygame.draw.rect(surface, color, rect, border_radius=12)

    # Draw button text
    draw_text(text, FONT, WHITE, surface, x + w // 2, y + h // 2)

    # Play action if clicked
    if hover and click[0] == 1 and action:
        if click_sound:
            click_sound.play()
        action()


# Run the game

main_menu()          