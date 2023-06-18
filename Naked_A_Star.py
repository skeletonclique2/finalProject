import pandas as pd
import random

def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def get_neighbors(locations, current):
    neighbors = []
    for floor, apartment in locations:
        if (floor == current[0] and abs(apartment - current[1]) == 1) or (apartment == current[1] and abs(floor - current[0]) == 1):
            neighbors.append((floor, apartment))
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

locations = [(floor, apartment) for floor in range(1, 9) for apartment in range(1, 6)]

apartments = pd.DataFrame(locations, columns=['Floor', 'Apartment'])

# Add boolean columns for broken_window, broken_lock, and intrusion variables
apartments['broken_window'] = False
apartments['broken_lock'] = False
apartments['both_broken'] = False

# Select a random apartment index
intrusion_index = random.randint(0, len(locations) - 1)

# Randomly set either or both variables to True for the selected apartment
apartments.loc[intrusion_index, 'broken_window'] = random.choice([True, False])
apartments.loc[intrusion_index, 'broken_lock'] = random.choice([True, False])

# Set the intrusion variable to True if both broken_window and broken_lock variables are True
apartments.loc[(apartments['broken_window'] == True) & (apartments['broken_lock'] == True), 'both_broken'] = True

# Search and print the apartment with either or both variables set to True
filtered_apartments = apartments.loc[(apartments['broken_window'] == True) | (apartments['broken_lock'] == True)]

print("Found the Intrusion!")
for _, apartment in filtered_apartments.iterrows():
    print(f"Floor: {apartment['Floor']}, Apartment: {apartment['Apartment']}")

# Perform A* search for each end apartment
print("\nIntrusion Path:")
for _, apartment in filtered_apartments.iterrows():
    start_apartment = (1, 1)
    end_apartment = (apartment['Floor'], apartment['Apartment'])

    open_set = [start_apartment]
    came_from = {}
    g_score = {start_apartment: 0}
    f_score = {start_apartment: heuristic(start_apartment, end_apartment)}

    while open_set:
        current = min(open_set, key=lambda apt: f_score[apt])

        if current == end_apartment:
            path = reconstruct_path(came_from, current)
            for apt in path:
                print(f"Floor: {apt[0]}, Apartment: {apt[1]}")
            break

        open_set.remove(current)

        for neighbor in get_neighbors(apartments[['Floor', 'Apartment']].values.tolist(), current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_apartment)
                if neighbor not in open_set:
                    open_set.append(neighbor)

print("\nApartment DataFrame:")
print(apartments)