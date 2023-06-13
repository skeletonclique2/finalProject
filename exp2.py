import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Intruder Detection and Localization")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)

# Define apartment dimensions and positions
apartment_width = 80
apartment_height = 80
apartment_padding = 30
floor_height = (window_height - apartment_padding * 7) / 6

# Define intruder dimensions
intruder_width = 60
intruder_height = 60

# Create a list of apartments and set initial status
apartments = []
for floor in range(6):
    for apartment in range(4):
        x = apartment_padding + apartment * (apartment_width + apartment_padding)
        y = apartment_padding + floor * (floor_height + apartment_padding)
        apartment_rect = pygame.Rect(x, y, apartment_width, apartment_height)
        apartment_info = {
            'rect': apartment_rect,
            'broken_window': False,
            'broken_lock': False
        }
        apartments.append(apartment_info)

# Function to randomize and place the intruder
def randomize_intruder():
    global intruder_apartment
    intruder_apartment = random.choice(apartments)

# Create the randomize button
button_width = 120
button_height = 40
button_x = window_width - button_width - 30
button_y = window_height - 80
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Initialize intruder location
intruder_apartment = None

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and button_rect.collidepoint(event.pos):
                randomize_intruder()

    # Clear the window
    window.fill(black)

    # Draw apartments
    for apartment_info in apartments:
        apartment_rect = apartment_info['rect']
        if apartment_info['broken_window'] or apartment_info['broken_lock']:
            pygame.draw.rect(window, red, apartment_rect)
        else:
            pygame.draw.rect(window, gray, apartment_rect)
        pygame.draw.rect(window, white, apartment_rect, 4)

    # Draw intruder if it's assigned
    if intruder_apartment is not None:
        intruder_rect = pygame.Rect(intruder_apartment['rect'].centerx - intruder_width / 2,
                                    intruder_apartment['rect'].centery - intruder_height / 2,
                                    intruder_width, intruder_height)
        pygame.draw.rect(window, red, intruder_rect)

    # Draw the randomize button
    pygame.draw.rect(window, green, button_rect)
    button_font = pygame.font.Font(None, 28)
    button_text = button_font.render("Randomize", True, black)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    window.blit(button_text, button_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()