import pandas as pd
import random

def find_path(adjacency_matrix, start, goal):
    stack = [(start, [])]
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path + [node]
        for neighbor in adjacency_matrix[node]:
            if neighbor not in path:
                stack.append((neighbor, path + [node]))
    return None

adjacency_matrix = {
    (1, 1): [(1, 2)],
    (1, 2): [(1, 1), (1, 3)],
    (1, 3): [(1, 2), (1, 4)],
    (1, 4): [(1, 3), (1, 5)],
    (1, 5): [(1, 4)],
    (2, 1): [(2, 2)],
    (2, 2): [(2, 1), (2, 3)],
    (2, 3): [(2, 2), (2, 4)],
    (2, 4): [(2, 3), (2, 5)],
    (2, 5): [(2, 4)],
    (3, 1): [(3, 2)],
    (3, 2): [(3, 1), (3, 3)],
    (3, 3): [(3, 2), (3, 4)],
    (3, 4): [(3, 3), (3, 5)],
    (3, 5): [(3, 4)],
    (4, 1): [(4, 2)],
    (4, 2): [(4, 1), (4, 3)],
    (4, 3): [(4, 2), (4, 4)],
    (4, 4): [(4, 3), (4, 5)],
    (4, 5): [(4, 4)],
    (5, 1): [(5, 2)],
    (5, 2): [(5, 1), (5, 3)],
    (5, 3): [(5, 2), (5, 4)],
    (5, 4): [(5, 3), (5, 5)],
    (5, 5): [(5, 4)],
    (6, 1): [(6, 2)],
    (6, 2): [(6, 1), (6, 3)],
    (6, 3): [(6, 2), (6, 4)],
    (6, 4): [(6, 3), (6, 5)],
    (6, 5): [(6, 4)],
    (7, 1): [(7, 2)],
    (7, 2): [(7, 1), (7, 3)],
    (7, 3): [(7, 2), (7, 4)],
    (7, 4): [(7, 3), (7, 5)],
    (7, 5): [(7, 4)],
    (8, 1): [(8, 2)],
    (8, 2): [(8, 1), (8, 3)],
    (8, 3): [(8, 2), (8, 4)],
    (8, 4): [(8, 3), (8, 5)],
    (8, 5): [(8, 4)]
}

locations = [(floor, apartment) for floor in range(1, 9) for apartment in range(1, 6)]

apartments = pd.DataFrame(locations, columns=['Floor', 'Apartment'])
apartments['broken'] = False

intrusion_index = random.randint(0, len(locations) - 1)
apartments.loc[intrusion_index, 'broken'] = True

intrusion_apartment = apartments.loc[intrusion_index]

print("Intrusion Detected!")
print(f"Floor: {intrusion_apartment['Floor']}, Apartment: {intrusion_apartment['Apartment']}")

neighbor_apartments = apartments.loc[(apartments['Floor'] == intrusion_apartment['Floor'] - 1) |
                                     (apartments['Floor'] == intrusion_apartment['Floor'] + 1) |
                                     (apartments['Apartment'] == intrusion_apartment['Apartment'] - 1) |
                                     (apartments['Apartment'] == intrusion_apartment['Apartment'] + 1)]

evacuation_paths = []
for _, neighbor in neighbor_apartments.iterrows():
    path = find_path(adjacency_matrix, (intrusion_apartment['Floor'], intrusion_apartment['Apartment']),
                     (neighbor['Floor'], neighbor['Apartment']))
    if path:
        evacuation_paths.append((neighbor, path))

if evacuation_paths:
    print("\nEvacuation Paths:")
    for neighbor, path in evacuation_paths:
        print(f"From: Floor {intrusion_apartment['Floor']}, Apartment {intrusion_apartment['Apartment']}")
        print(f"To: Floor {neighbor['Floor']}, Apartment {neighbor['Apartment']}")
        print("Path:", path)
else:
    print("\nNo neighboring apartments to evacuate.")
