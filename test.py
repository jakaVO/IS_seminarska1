# Treba za naredit:
# Pri generate_random_tree ne sme pridt do digit to digit operacij (enkrat sm dubu 9**5 kot del expressiona)

from functions import *
import numpy as np
import random
import pandas as pd

solution = ""

row_index = 41
df = pd.read_csv("data.csv")
x_values = df["Xs"].iloc[row_index]
y_values = df["Ys"].iloc[row_index]
correct_solution = df["Equation"].iloc[row_index]
x_values = np.array(eval(x_values))
y_values = np.array(eval(y_values))


population_size = 100
max_generations = 10
mutation_rate = 2
number_of_parents = 1
max_base_population_tree_height = 1

def fitness(expression):
    try:
        predicted_y = []
        print("fitness")
        print_expression(expression)
        list_x = x_values.tolist()
        for xi in list_x:
            yi = evaluate(expression, int(xi))
            predicted_y.append(yi)
        mse = np.mean((np.array(predicted_y) - y_values) ** 2)
        print("mse: " + str(mse))
        return (1.0 / (mse + 1e-6), expression)  # Avoid division by zero
    except Exception as e:
        return (0.0, expression)  # Return a low fitness for invalid expressions

mytree = TreeNode("+")
mytree.left = TreeNode("/")
mytree.left.left = TreeNode("x")
mytree.left.right = TreeNode("3")
mytree.right = TreeNode("9")

mytree2 = TreeNode("/")
mytree2.left = TreeNode("x")
mytree2.right = TreeNode("3")

population = []
population.append(mytree)
population.append(mytree2)
# Create an initial population
population += [generate_random_tree(max_base_population_tree_height) for _ in range(population_size)]
for i in range(len(population)):
    print_expression(population[i])

# Main genetic algorithm loop
for generation in range(max_generations):
    print("zacetek nove")
    # Evaluate fitness for each individual
    fitness_scores = [fitness(individual) for individual in population]
    print([x[0] for x in fitness_scores])

    # Select parents based on fitness scores (roulette wheel selection)
    selected_parents = sorted(fitness_scores, key=lambda x: x[0], reverse=True)[:number_of_parents]

    print("Pa še selected:")
    for i in range(len(selected_parents)):
        print_expression(selected_parents[i][1])

    if selected_parents[0][0] == 1000000.0:
        population = [x[1] for x in selected_parents]
        print("najdena")
        break

    print("asd")

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

    print("Nova populacija:")
    for i in range(len(population)):
        print_expression(population[i])

best_individual = population[0]
print(population)

print("Best Equation:")
print_expression(best_individual)
print("Correct equation:")
print(correct_solution)