import random
from queue import PriorityQueue

from pycsp3 import Problem, Var, And, Or, Not, Xor, leq, eq

from choco.solver import ChocoSolver

# Define the apartments
apartments = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2), (2, 3), (2, 4),
    (3, 1), (3, 2), (3, 3), (3, 4),
    (4, 1), (4, 2), (4, 3), (4, 4),
    (5, 1), (5, 2), (5, 3), (5, 4),
    (6, 1), (6, 2), (6, 3), (6, 4)
]

# Randomly assign broken_window and broken_lock to the same apartment
broken_apartment = random.choice(apartments)

broken_window_floor, broken_window_apartment = broken_apartment
broken_lock_floor, broken_lock_apartment = broken_apartment

# Create a CSP problem instance
problem = ChocoSolver()

# Define the variables
apartment = problem.IntVar("apartment", apartments)

# Define the constraints
problem.AddConstraint(apartment in apartments)
problem.AddConstraint(Not(apartment == broken_apartment))

# Solve the CSP problem
solution = problem.Solve()

# If a solution was found, find the shortest path to the intruder's location
if solution is not None:
    apartment = solution[apartment]

    # Find the shortest path to the intruder's location using A* searching
    shortest_path = find_shortest_path(broken_window_floor, broken_window_apartment, apartment)

    if shortest_path is not None:
        print("Shortest path to reach the intruder's location:")
        for floor, apartment in shortest_path:
            print("Floor: {}, Apartment: {}".format(floor, apartment))
    else:
        print("No path found to reach the intruder's location.")
else:
    print("No solution found.")
