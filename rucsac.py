import random


# Funcția pentru generarea populației inițiale
def generate_population(size, n_items):
    return [[random.randint(0, 1) for _ in range(n_items)] for _ in range(size)]


# Funcția de fitness
def fitness(individual, weights, values, capacity):
    total_weight = sum(w * i for w, i in zip(weights, individual))
    total_value = sum(v * i for v, i in zip(values, individual))
    if total_weight > capacity:
        return 0  # Penalizare pentru depășirea capacității
    return total_value


# Selectarea părinților folosind selecția turnirului
def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(range(len(population)), k)
    best = max(selected, key=lambda idx: fitnesses[idx])
    return population[best]


# Crossover între doi părinți
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# Mutarea unui individ
def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # Schimbă 0 în 1 sau invers
    return individual


# Algoritmul genetic pentru problema rucsacului
def genetic_algorithm(weights, values, capacity, population_size=100, generations=100, mutation_rate=0.01):
    n_items = len(weights)
    population = generate_population(population_size, n_items)

    for generation in range(generations):
        fitnesses = [fitness(ind, weights, values, capacity) for ind in population]

        # Crearea unei noi generații
        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, mutation_rate))

        population = new_population

    # Returnarea celui mai bun individ din populație
    fitnesses = [fitness(ind, weights, values, capacity) for ind in population]
    best_idx = fitnesses.index(max(fitnesses))
    return population[best_idx], max(fitnesses)


# Exemplu de utilizare
if __name__ == "__main__":
    weights = [10, 20, 30, 40, 50]
    values = [60, 100, 120, 140, 160]
    capacity = 100
    best_solution, best_value = genetic_algorithm(weights, values, capacity)
    print("Cea mai bună soluție:", best_solution)
    print("Valoarea totală:", best_value)
