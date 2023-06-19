import pandas as pd
import random
from constraint import Problem, AllDifferentConstraint

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

# Perform CSP using backtracking for each end apartment
print("\nIntrusion Path:")

def constraint(A, a, B, b):
    return a != b

for _, apartment in filtered_apartments.iterrows():
    start_apartment = (1, 1)
    end_apartment = (apartment['Floor'], apartment['Apartment'])

    problem = Problem()
    variables = [(i, j) for i in range(1, 9) for j in range(1, 6)]
    problem.addVariables(variables, apartments['Apartment'].values.tolist())

    for var in variables:
        neighbors = get_neighbors(variables, var)
        problem.addConstraint(AllDifferentConstraint(), neighbors)

    problem.addConstraint(constraint, [start_apartment, end_apartment])

    solution = problem.getSolution()

    if solution is not None:
        path = reconstruct_path(solution, start_apartment)
        for apt in path:
            print(f"Floor: {apt[0]}, Apartment: {apt[1]}")

print("\nApartment DataFrame:")
print(apartments)
