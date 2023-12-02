# Treba za naredit:
# Pri generate_random_tree ne sme pridt do digit to digit operacij (enkrat sm dubu 9**5 kot del expressiona)
# Treba zagotovit, da se pri novi populaciji ne bojo ponavljal expressioni (npr. men se kdaj zgodi da so prvi štirje najboljši "x**4" vsi enaki)

from functions import *
import numpy as np
import random
import pandas as pd
from matplotlib import pyplot as plt

solution = ""

row_index = 30
df = pd.read_csv("data.csv")
x_values = df["Xs"].iloc[row_index]
y_values = df["Ys"].iloc[row_index]
correct_solution = df["Equation"].iloc[row_index]
x_values = np.array(eval(x_values))
y_values = np.array(eval(y_values))
# print(y_values.tolist())

# plt.plot(x_values, y_values)
# plt.xlabel('X-axis label')
# plt.ylabel('Y-axis label')
# plt.show()


population_size = 1000
max_generations = 2000
mutation_rate = 1
number_of_parents = 3
max_base_population_tree_height = 1
debugging_mode = False # For printing out results of various functions during the code run

def fitness(expression):
    try:
        predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
        dif_squared_arr = []
        for i in range(len(y_values)):
            if (predicted_y[i] - y_values[i] > 10000000):
                continue
            dif_squared = np.power((predicted_y[i] - y_values[i]), 2)
            dif_squared_arr.append(dif_squared)
        mse = np.mean(np.array(dif_squared_arr))
        return (1.0 / (mse + 1e-6), expression)  # Avoid division by zero
    except Exception as e:
        return (0.0, expression)  # Return a low fitness for invalid expressions

population = []
population += [generate_random_tree(max_base_population_tree_height) for _ in range(population_size)]
if debugging_mode:
    print("Initial population: ", end="")
    print_expressions(population)

for generation in range(max_generations):
    fitness_scores = [fitness(individual) for individual in population]

    selected_parents = sorted(fitness_scores, key=lambda x: x[0], reverse=True)[:number_of_parents]

    if debugging_mode:
        print("Selected parents for next generation: ", end="")
        print_expressions([x[1] for x in selected_parents])

    if selected_parents[0][0] == 1000000.0:
        population = [x[1] for x in selected_parents]
        print("Najdena predčasno!")
        break

    new_population = [t[1] for t in selected_parents]

    i = 0
    while len(new_population) < population_size:
        # parent1, parent2 = random.choices(selected_parents, k=2)
        # parent1 = parent1[1]
        # parent2 = parent2[1]
        # crossover_point = random.randint(1, len(parent1) - 1)
        # child = parent1[:crossover_point] + parent2[crossover_point:]

        child = tree_copy(new_population[i])
        
        child = mutate(child, mutation_rate)

        new_population.append(child)

        if i + 1 == number_of_parents:
            i = 0
        else:
            i += 1
    if debugging_mode:
        print("Nova populacija: ", end="")
        print_expressions(new_population)

    population = new_population

best_individual = population[0]

print("Best Equation:")
print_expression(best_individual)
print("Correct equation:")
print(correct_solution)