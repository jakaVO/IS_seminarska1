from functions import *
import numpy as np
import random

solution = ""

x_values = np.array([1, 2, 3])
y_values = np.array([5, 6, 7])

population_size = 100
max_generations = 100
mutation_rate = 0.5
number_of_parents = 10

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
operators = ['+', '-', '*', '/']

# Generate a random individual (equation)
def generate_individual(equation = ""):
    if (equation == ""):
        equation = 'x'
        equation += random.choice(operators)
        equation += random.choice(digits)
    else:
        changeOperator = random.getrandbits(1)
        if (changeOperator == 1):
            equation[1] = random.choice(operators)
        else:
            equation[2] = random.choice(digits)
    return equation

def fitness(expression):
    expression_to_evaluate = f"lambda x: {expression}"
    try:
        function = eval(expression_to_evaluate)
        predicted_y = [function(xi) for xi in x_values]
        mse = np.mean((np.array(predicted_y) - y_values) ** 2)
        return (1.0 / (mse + 1e-3), expression)  # Avoid division by zero
    except Exception as e:
        return (0.0, expression)  # Return a low fitness for invalid expressions

# Create an initial population
population = [generate_individual() for _ in range(population_size)]

# Main genetic algorithm loop
for generation in range(max_generations):
    # Evaluate fitness for each individual
    fitness_scores = [fitness(individual) for individual in population]

    # Select parents based on fitness scores (roulette wheel selection)
    selected_parents = sorted(fitness_scores, key=lambda x: x[0], reverse=True)[:number_of_parents]

    print(selected_parents[0])

    # Create a new population through crossover and mutation
    new_population = [t[1] for t in selected_parents]

    while len(new_population) < population_size:
        parent1, parent2 = random.choices(selected_parents, k=2)
        parent1 = parent1[1]
        parent2 = parent2[1]
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        
        # Apply mutation
        if random.random() < mutation_rate:
            mutation_point = random.randint(1, len(child) - 1)
            if mutation_point == 1:
                mutated_gene = random.choice(operators)
            else:
                mutated_gene = random.choice(digits)
            child = child[:mutation_point] + mutated_gene + child[mutation_point + 1:]

        new_population.append(child)

    population = new_population

best_individual = sorted(population, key=lambda x: x[0], reverse=True)[0]

print("Best Equation:", best_individual)