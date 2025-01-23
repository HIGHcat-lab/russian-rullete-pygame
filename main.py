import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Russian Roulette")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 100)

# Sound Effect File Paths (MP3 and WAV)
revolver_sound_path = "revolver_shot.mp3"       # Add your revolver shot WAV file
game_over_sound_path = "game_over.mp3"         # Add your game over MP3 file
spinning_barrel_sound_path = "spinning_barrel.mp3"  # Add your spinning barrel WAV file
background_music_path = "background_music.mp3" # Add your background music MP3 file

# Load Sound Effects
revolver_sound = pygame.mixer.Sound(revolver_sound_path)
spinning_barrel_sound = pygame.mixer.Sound(spinning_barrel_sound_path)
pygame.mixer.init()

def play_music(file_path, loop=False):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1 if loop else 0)

def stop_music():
    pygame.mixer.music.stop()

# Play background music on loop
play_music(background_music_path, loop=True)

# Cylinder configuration
CYLINDER_RADIUS = 100
CYLINDER_CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_CHAMBERS = 6

# Game variables
bullet_position = random.randint(0, NUM_CHAMBERS - 1)
current_position = 0
game_over = False
message = "Spin the Cylinder!"
can_pull_trigger = False  # Prevent pulling the trigger until the cylinder has spun

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
SPIN_BUTTON = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 150, BUTTON_WIDTH, BUTTON_HEIGHT)
TRIGGER_BUTTON = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 75, BUTTON_WIDTH, BUTTON_HEIGHT)
EXIT_BUTTON = pygame.Rect(WIDTH - 110, 10, 100, 40)  # Exit button dimensions

# Function to draw the cylinder
def draw_cylinder(rotation_angle=0):
    for i in range(NUM_CHAMBERS):
        angle = (360 / NUM_CHAMBERS) * i + rotation_angle
        radians = math.radians(angle)
        x = CYLINDER_CENTER[0] + CYLINDER_RADIUS * 0.6 * math.cos(radians)
        y = CYLINDER_CENTER[1] + CYLINDER_RADIUS * 0.6 * math.sin(radians)

        # Draw chamber
        pygame.draw.circle(screen, GRAY, (int(x), int(y)), 20)

        # Highlight the current position
        if i == current_position:
            pygame.draw.circle(screen, GREEN, (int(x), int(y)), 25, 2)

# Function to animate the spinning of the cylinder
def spin_cylinder():
    global current_position, bullet_position, can_pull_trigger
    spinning_barrel_sound.play()  # Play spinning barrel sound
    for rotation_angle in range(0, 720, 20):  # Spin faster (720 degrees at 20-degree steps)
        screen.fill(WHITE)
        draw_cylinder(rotation_angle)
        pygame.draw.rect(screen, BLACK, SPIN_BUTTON)
        spin_text = font.render("Spinning...", True, WHITE)
        screen.blit(spin_text, (SPIN_BUTTON.x + 20, SPIN_BUTTON.y + 10))
        pygame.display.flip()
        pygame.time.delay(20)  # Faster delay
    spinning_barrel_sound.stop()  # Stop spinning barrel sound

    # Reset the bullet position and current position
    bullet_position = random.randint(0, NUM_CHAMBERS - 1)
    current_position = 0
    can_pull_trigger = True  # Allow pulling the trigger now

# Function to simulate the adrenaline rush effect
def adrenaline_rush_effect():
    oval_width, oval_height = 10, 10  # Start with a small oval
    while oval_width < WIDTH * 2 and oval_height < HEIGHT * 2:  # Expand until it fills the screen
        screen.fill(BLACK)

        # Draw the expanding oval
        pygame.draw.ellipse(screen, WHITE, (WIDTH // 2 - oval_width // 2, HEIGHT // 2 - oval_height // 2, oval_width, oval_height))
        oval_width += 30
        oval_height += 20
        pygame.display.flip()
        pygame.time.delay(50)

# Function to simulate the eye effect with a mouse-tracking oval
def eye_simulation():
    mask_width, mask_height = 300, 200  # Oval dimensions

    for _ in range(40):  # Eye effect lasts ~2 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render the game normally
        screen.fill(WHITE)
        draw_cylinder()
        pygame.draw.rect(screen, BLACK, SPIN_BUTTON)
        pygame.draw.rect(screen, BLACK, TRIGGER_BUTTON)
        spin_text = font.render("Spin Cylinder", True, WHITE)
        trigger_text = font.render("Pull Trigger", True, WHITE)
        screen.blit(spin_text, (SPIN_BUTTON.x + 20, SPIN_BUTTON.y + 10))
        screen.blit(trigger_text, (TRIGGER_BUTTON.x + 20, TRIGGER_BUTTON.y + 10))
        message_text = font.render(message, True, BLACK)
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, 50))

        # Create a black mask
        mask = pygame.Surface((WIDTH, HEIGHT))
        mask.fill(BLACK)

        # Cut out an oval around the mouse position
        pygame.draw.ellipse(mask, WHITE, (mouse_x - mask_width // 2, mouse_y - mask_height // 2, mask_width, mask_height))

        # Apply the mask to the screen
        screen.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        pygame.display.flip()
        pygame.time.delay(50)

def game_over_screen():
    while True:  # Infinite loop for the flashing game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and EXIT_BUTTON.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        # Flash red screen
        screen.fill(RED)
        game_over_text = game_over_font.render("GAME OVER", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.draw.rect(screen, BLACK, EXIT_BUTTON)
        exit_text = font.render("EXIT", True, WHITE)
        screen.blit(exit_text, (EXIT_BUTTON.x + 20, EXIT_BUTTON.y + 5))
        pygame.display.flip()
        pygame.time.delay(300)

        # Flash white screen
        screen.fill(WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.draw.rect(screen, BLACK, EXIT_BUTTON)
        screen.blit(exit_text, (EXIT_BUTTON.x + 20, EXIT_BUTTON.y + 5))
        pygame.display.flip()
        pygame.time.delay(300)


# Function to display the shrinking oval effect when dying
def shrinking_oval_effect():
    revolver_sound.play()  # Play the revolver shot sound
    stop_music()  # Stop background music
    play_music(game_over_sound_path)  # Start playing the game over sound
    oval_width, oval_height = 300, 200  # Starting oval dimensions
    while oval_width > 0 and oval_height > 0:
        screen.fill(BLACK)

        # Draw the shrinking oval
        pygame.draw.ellipse(screen, WHITE,
                            (WIDTH // 2 - oval_width // 2, HEIGHT // 2 - oval_height // 2, oval_width, oval_height))
        oval_width -= 5
        oval_height -= 3
        pygame.display.flip()
        pygame.time.delay(50)

    # After shrinking the oval, transition to the game over screen
    game_over_screen()


# Main game loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if SPIN_BUTTON.collidepoint(event.pos) and not game_over:
                spin_cylinder()
                message = "Cylinder Spun! Pull the Trigger!"
            elif TRIGGER_BUTTON.collidepoint(event.pos) and can_pull_trigger:
                eye_simulation()  # Trigger the eye simulation effect
                if current_position == bullet_position:
                    shrinking_oval_effect()  # Show the shrinking oval effect
                    while True:  # Loop for game over
                        pass
                else:
                    current_position = (current_position + 1) % NUM_CHAMBERS
                    message = "Click... You're safe!"
                    adrenaline_rush_effect()  # Trigger the adrenaline rush effect

    # Draw cylinder
    draw_cylinder()

    # Draw buttons
    pygame.draw.rect(screen, BLACK, SPIN_BUTTON)
    pygame.draw.rect(screen, BLACK, TRIGGER_BUTTON)

    # Draw button text
    spin_text = font.render("Spin Cylinder", True, WHITE)
    trigger_text = font.render("Pull Trigger", True, WHITE)
    screen.blit(spin_text, (SPIN_BUTTON.x + 20, SPIN_BUTTON.y + 10))
    screen.blit(trigger_text, (TRIGGER_BUTTON.x + 20, TRIGGER_BUTTON.y + 10))

    # Draw message
    message_text = font.render(message, True, BLACK)
    screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, 50))

    # Disable the trigger button if spinning isn't done yet
    if not can_pull_trigger:
        pygame.draw.rect(screen, GRAY, TRIGGER_BUTTON)

    pygame.display.flip()
    clock.tick(30)
