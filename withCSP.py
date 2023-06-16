import random
from queue import PriorityQueue
from constraint import Problem, AllDifferentConstraint

apartments = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2), (2, 3), (2, 4),
    (3, 1), (3, 2), (3, 3), (3, 4),
    (4, 1), (4, 2), (4, 3), (4, 4),
    (5, 1), (5, 2), (5, 3), (5, 4),
    (6, 1), (6, 2), (6, 3), (6, 4)
]

def randomize_burglar():
    X = random.randint(1, 6)
    Y = random.randint(1, 4)
    return (X, Y)

burglar = randomize_burglar()

def goal(X, Y):
    return (X, Y) == burglar

def heuristic(X, Y):
    Xg, Yg = burglar
    return abs(X - Xg) + abs(Y - Yg)

def move(X, Y):
    possible_moves = []
    if (X + 1, Y) in apartments:
        possible_moves.append((X + 1, Y))
    if (X - 1, Y) in apartments:
        possible_moves.append((X - 1, Y))
    if (X, Y + 1) in apartments:
        possible_moves.append((X, Y + 1))
    if (X, Y - 1) in apartments:
        possible_moves.append((X, Y - 1))
    if X == 1:
        if (X, Y + 1) in apartments:
            possible_moves.append((X, Y + 1))
        if (X, Y - 1) in apartments:
            possible_moves.append((X, Y - 1))
    elif X == 6:
        if (X, Y + 1) in apartments:
            possible_moves.append((X, Y + 1))
        if (X, Y - 1) in apartments:
            possible_moves.append((X, Y - 1))
    else:
        if (X, Y + 1) in apartments:
            possible_moves.append((X, Y + 1))
        if (X, Y - 1) in apartments:
            possible_moves.append((X, Y - 1))
        if (X, Y + 1) in apartments:
            possible_moves.append((X, Y + 1))
        if (X, Y - 1) in apartments:
            possible_moves.append((X, Y - 1))
    return possible_moves

def find_shortest_paths():
    start = (1, 1)

    problem = Problem()
    problem.addVariables(range(1, 5), apartments)
    problem.addConstraint(AllDifferentConstraint())

    solutions = problem.getSolutions()

    shortest_paths = []

    for solution in solutions:
        target = solution[1]  # Neighboring apartment

        distances = {apartment: float('inf') for apartment in apartments}
        distances[start] = 0

        queue = PriorityQueue()
        queue.put((0, start))

        previous = {apartment: None for apartment in apartments}

        while not queue.empty():
            _, current = queue.get()

            if current == target:
                break

            for next_apartment in move(*current):
                distance = distances[current] + 1
                if distance < distances[next_apartment]:
                    distances[next_apartment] = distance
                    previous[next_apartment] = current

                    priority = distance + heuristic(*next_apartment)
                    queue.put((priority, next_apartment))

        if previous[target] is not None:
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            shortest_paths.append(path)

    return shortest_paths

# Call the function
shortest_paths = find_shortest_paths()

if shortest_paths:
    print("Shortest paths to reach the neighboring apartments:")
    for path in shortest_paths:
        for floor, apartment in path:
            print("Floor: {}, Apartment: {}".format(floor, apartment))
        print("---")
else:
    print("No paths found to reach the neighboring apartments.")
