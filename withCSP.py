import random
from queue import PriorityQueue

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

def find_shortest_path(X, Y):
    start = (1, 1)
    target = (X, Y)

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
        return path

    return None


# Define the CSP class
class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint in self.constraints:
            if var in constraint:
                neighbor = constraint[0] if constraint[0] != var else constraint[1]
                if neighbor in assignment and assignment[neighbor] == value:
                    return False
        return True


# Construct the CSP
variables = apartments[4:]
domains = {var: apartments for var in variables}
constraints = [(var1, var2) for i, var1 in enumerate(variables) for var2 in variables[i + 1:]]
csp = CSP(variables, domains, constraints)

# Find the solution using CSP
csp_solution = csp.backtrack({})

# Print the shortest paths to each neighboring apartment
if csp_solution is not None:
    print("Shortest paths to reach the neighboring apartments:")
    for var, apartment in csp_solution.items():
        path = find_shortest_path(apartment[0], apartment[1])
        if path is not None:
            print("Apartment: {}, Path: {}".format(var, path))
else:
    print("No solution found for the neighboring apartments.")
