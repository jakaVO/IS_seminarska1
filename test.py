from functions import *
import numpy as np
import random
import pandas as pd

solution = ""

df = pd.read_csv("data.txt")
selected_row = df.iloc[29]
x_values = np.array(selected_row["Xs"])
y_values = np.array(selected_row["Ys"])

population_size = 100
max_generations = 100
mutation_rate = 1
number_of_parents = 10
max_base_population_tree_height = 5

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

    if fitness(selected_parents[0][1]) == 1000.0:
        population = selected_parents
        break

    # Create a new population through crossover and mutation
    new_population = [t[1] for t in selected_parents]

    i = 0
    while len(new_population) < population_size:
        # parent1, parent2 = random.choices(selected_parents, k=2)
        # parent1 = parent1[1]
        # parent2 = parent2[1]
        # crossover_point = random.randint(1, len(parent1) - 1)
        # child = parent1[:crossover_point] + parent2[crossover_point:]

        child = tree_copy(new_population[i])
        
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
print_expression(best_individual)