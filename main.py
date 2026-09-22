import random
import math


# Визначення функції Сфери
def sphere_function(x):
    return sum(xi ** 2 for xi in x)


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    current_points = [random.uniform(bound[0], bound[1]) for bound in bounds]
    current_value = func(current_points)

    # Функція для визначення сусідів поточної точки
    def get_neighbors(current, bounds, step_size=0.1):
        x1, x2 = current
        neighbors = [
            (x1 + step_size, x2),
            (x1 - step_size, x2),
            (x1, x2 + step_size),
            (x1, x2 - step_size)
        ]
        valid_neighbors = []
        for neighbor in neighbors:
            if (bounds[0][0] <= neighbor[0] <= bounds[0][1] and
                bounds[1][0] <= neighbor[1] <= bounds[1][1]):
                valid_neighbors.append(neighbor)
        return valid_neighbors

    for _ in range(iterations):
        neighbors = get_neighbors(current_points, bounds)
        # Пошук найкращого сусіда
        next_point = None
        next_value = float('inf')
        for neighbor in neighbors:
            value = func(neighbor)
            if value < next_value:
                next_point = neighbor
                next_value = value

        if current_value - next_value < epsilon:
            break
        # Переходимо до кращого сусіда
        current_points, current_value = next_point, next_value

    return current_points, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    # Функція для визначення випадкового сусіда
    def get_random_neighbor(current, bounds, step_size=0.5):
        x, y = current
        while True:
            new_x = x + random.uniform(-step_size, step_size)
            new_y = y + random.uniform(-step_size, step_size)
            if (bounds[0][0] <= new_x <= bounds[0][1] and bounds[1][0] <= new_y <= bounds[1][1]):
                return (new_x, new_y)
    step_size = 0.5
    probability = 0.2
    current_points = tuple(random.uniform(bound[0], bound[1]) for bound in bounds)
    current_value = func(current_points)

    for _ in range(iterations):
        # Отримання випадкового сусіда
        new_point = get_random_neighbor(current_points, bounds, step_size)
        new_value = func(new_point)

        old_points = current_points
        # Перевірка умови переходу
        if new_value < current_value or random.random() < probability:
            current_points, current_value = new_point, new_value

            if (math.dist(old_points, current_points) < epsilon):
                break
    return current_points, current_value
    

# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    def generate_neighbor(solution):
        x, y = solution
        while True:
            new_x = x + random.uniform(-1, 1)
            new_y = y + random.uniform(-1, 1)
            if (bounds[0][0] <= new_x <= bounds[0][1] and bounds[1][0] <= new_y <= bounds[1][1]):
                return (new_x, new_y)
    current_points = tuple(random.uniform(bound[0], bound[1]) for bound in bounds)
    current_energy = func(current_points)
    for _ in range(iterations):
        new_points = generate_neighbor(current_points)
        new_energy = func(new_points)
        delta_energy = new_energy - current_energy
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temp):
            current_points = new_points
            current_energy = new_energy
        temp *= cooling_rate
        if temp < epsilon:
            break
    return current_points, current_energy


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]
    
    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
