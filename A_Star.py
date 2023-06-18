import pandas as pd
import random

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


def a_star_search(graph, start, goal):
    open_set = set([start])
    came_from = {}
    g_score = {apartment: float('inf') for apartment in graph}
    g_score[start] = 0
    f_score = {apartment: float('inf') for apartment in graph}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda apartment: f_score[apartment])
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        for neighbor in get_neighbors(graph, current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None


# Define heuristic function
def heuristic(apartment, goal):
    return abs(apartment[0] - goal[0]) + abs(apartment[1] - goal[1])

# Define function to get neighboring apartments
def get_neighbors(graph, apartment):
    neighbors = []
    floor, apt = apartment

    # Check neighboring apartments within the same floor
    if apt > 1:
        neighbors.append((floor, apt - 1))
    if apt < 5:
        neighbors.append((floor, apt + 1))

    # Check neighboring apartments on the previous and next floors
    if floor > 1:
        neighbors.append((floor - 1, apt))
        neighbors.append((floor - 1, 1))
    if floor < 8:
        neighbors.append((floor + 1, apt))
        neighbors.append((floor + 1, 1))

    return neighbors

# Define function to reconstruct the path from start to end
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


# Set the start apartment
start_apartment = (1, 1)

# Set the end apartment based on the 'both_broken' variable
end_apartments = apartments[(apartments['both_broken'] == True)][['Floor', 'Apartment']].values.tolist()

# Perform A* search for each end apartment
for end_apartment in end_apartments:
    intrusion_path = a_star_search(apartments[['Floor', 'Apartment']].values.tolist(), start_apartment, tuple(end_apartment))
    print("\nIntrusion Path:")
    for apartment in intrusion_path:
        print(f"Floor: {apartment[0]}, Apartment: {apartment[1]}")

# Print the DataFrame
print("\nApartment DataFrame:")
print(apartments)
