from functions import *
import numpy as np
import random

solution = ""

x_values = np.array([1, 2, 3])
y_values = np.array([5, 6, 7])

population_size = 10
max_generations = 2
mutation_rate = 1
number_of_parents = 2
max_base_population_tree_height = 1

def fitness(expression):
    try:
        predicted_y = [evaluate(expression, xi) for xi in x_values]
        mse = np.mean((np.array(predicted_y) - y_values) ** 2)
        return (1.0 / (mse + 1e-3), expression)  # Avoid division by zero
    except Exception as e:
        return (0.0, expression)  # Return a low fitness for invalid expressions

# Create an initial population
population = [generate_random_tree(max_base_population_tree_height) for _ in range(population_size)]

# Main genetic algorithm loop
for generation in range(max_generations):
    # Evaluate fitness for each individual
    fitness_scores = [fitness(individual) for individual in population]

    # Select parents based on fitness scores (roulette wheel selection)
    selected_parents = sorted(fitness_scores, key=lambda x: x[0], reverse=True)[:number_of_parents]

    print_tree(selected_parents[0][1])

    if fitness(selected_parents[0][1]) == 1000.0:
        population = selected_parents
        break

    # print(selected_parents[0])

    # Create a new population through crossover and mutation
    new_population = [t[1] for t in selected_parents]

    i = 0
    while len(new_population) < population_size:
        # parent1, parent2 = random.choices(selected_parents, k=2)
        # parent1 = parent1[1]
        # parent2 = parent2[1]
        # crossover_point = random.randint(1, len(parent1) - 1)
        # child = parent1[:crossover_point] + parent2[crossover_point:]

        child = new_population[i]
        
        # Apply mutation
        child = mutate(child, mutation_rate)

        new_population.append(child)

        if i + 1 == number_of_parents:
            i = 0
        else:
            i += 1

    population = new_population

best_individual = population[0]

print("Best Equation:")
print_tree(best_individual)