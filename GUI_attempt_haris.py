import pygame
import pandas as pd
import random

# Pygame initialization
pygame.init()
clock = pygame.time.Clock()

# Window dimensions
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Apartment Intrusion Search")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font initialization
pygame.font.init()
font_large = pygame.font.SysFont("Arial", 30)
font_medium = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 16)

def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


# Function to draw the apartment grid
def draw_grid(apartments):
    apartment_width = window_width / 6
    apartment_height = window_height / 9
    margin = 10

    for i, row in apartments.iterrows():
        floor = row["Floor"]
        apartment = row["Apartment"]
        x = (apartment - 1) * apartment_width + margin
        y = (floor - 1) * apartment_height + margin
        rect = pygame.Rect(x, y, apartment_width - 2 * margin, apartment_height - 2 * margin)

        if row["Broken Window"] or row["Broken Lock"]:
            pygame.draw.rect(window, (255, 0, 0), rect)
        else:
            pygame.draw.rect(window, white, rect, 1)

        draw_text(str(floor) + "-" + str(apartment), font_small, black, x + apartment_width / 2,
                  y + apartment_height / 2)


# Create the DataFrame of apartments
locations = [(floor, apartment) for floor in range(1, 9) for apartment in range(1, 6)]
apartments = pd.DataFrame(locations, columns=["Floor", "Apartment"])
apartments["Broken Window"] = False
apartments["Broken Lock"] = False

# Select a random apartment index
intrusion_index = random.randint(0, len(locations) - 1)
apartments.loc[intrusion_index, "Broken Window"] = random.choice([True, False])
apartments.loc[intrusion_index, "Broken Lock"] = random.choice([True, False])

# Animation variables
animation_delay = 2000  # Delay between animation steps in milliseconds
current_animation_step = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill(white)

    if current_animation_step == 0:
        if not apartments.loc[intrusion_index, "Broken Window"] and not apartments.loc[intrusion_index, "Broken Lock"]:
            draw_text("There was no Break-In found!!", font_large, black, window_width / 2, window_height / 2 - 50)
            draw_text("Your Apartment Building is Safe :))", font_large, black, window_width / 2,
                      window_height / 2 + 50)
            draw_text("Apartment DataFrame:", font_large, black, window_width / 2, window_height - 100)
            draw_grid(apartments)
        else:
            filtered_apartments = apartments.loc[
                (apartments["Broken Window"] == True) | (apartments["Broken Lock"] == True)
                ]

            draw_text("Found the Intrusion at", font_large, black, window_width / 2, 50)
            for _, apartment in filtered_apartments.iterrows():
                draw_text(
                    f"Floor: {apartment['Floor']}, Apartment: {apartment['Apartment']}",
                    font_medium,
                    black,
                    window_width / 2,
                    window_height / 2 - 50,
                )

            floor_to_evacuate = apartments.loc[intrusion_index, "Floor"]
            draw_text("Please Evacuate the " + str(floor_to_evacuate) + "th FLOOR", font_large, black, window_width / 2,
                      window_height / 2 + 50)

    elif current_animation_step == 1:
        draw_text("Shortest Path to the Apartment Intrusion is found at:", font_large, black, window_width / 2, 50)

        for _, apartment in filtered_apartments.iterrows():
            start_apartment = (1, 1)
            end_apartment = (apartment["Floor"], apartment["Apartment"])
            path = []

            open_set = [start_apartment]
            came_from = {}
            g_score = {start_apartment: 0}
            f_score = {start_apartment: heuristic(start_apartment, end_apartment)}

            try:
                while open_set:
                    current = min(open_set, key=lambda apt: f_score[apt])

                    if current == end_apartment:
                        path = reconstruct_path(came_from, current)
                        break

                    open_set.remove(current)

                    for neighbor in get_neighbors(apartments[["Floor", "Apartment"]].values.tolist(), current):
                        tentative_g_score = g_score[current] + 1

                        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_apartment)
                            if neighbor not in open_set:
                                open_set.append(neighbor)
                else:
                    raise Exception("No path found to the end apartment.")

            except Exception as e:
                draw_text(str(e), font_medium, black, window_width / 2, window_height / 2 - 50)

            for apt in path:
                draw_text(f"Floor: {apt[0]}, Apartment: {apt[1]}", font_small, black, window_width / 2,
                          window_height / 2 + 50)

    elif current_animation_step == 2:
        draw_text("Apartment DataFrame:", font_large, black, window_width / 2, 50)
        draw_grid(apartments)

    current_animation_step += 1
    if current_animation_step > 2:
        current_animation_step = 0

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

    # Delay before next animation step
    pygame.time.delay(animation_delay)

# Quit the game
pygame.quit()
