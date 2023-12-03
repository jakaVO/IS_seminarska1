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

all_best_fitness_scores = []
all_mutation_rates = []
fresh_parents_to_add = 0

fitness_weight = 0.05
population_size = 250
max_generations = 2500
mutation_rate = 0.2
number_of_parents = 100
max_base_population_tree_height = 1
debugging_mode = True # For printing out results of various functions during the code run

def fitness1(expression):
    try:
        predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
        dif_squared_arr = []
        for i in range(len(y_values)):
            if predicted_y[i] > 10000000000:
                return (-1.0, expression)
            # dif_squared = np.power((np.log(np.abs(predicted_y[i]) + 1e-6) - np.log(np.abs(y_values[i]) + 1e-6)), 2)
            dif_squared = np.power(predicted_y[i] - y_values[i], 2)
            dif_squared_arr.append(dif_squared)
        mse = np.mean(np.array(dif_squared_arr))
        if mse > 10000000000:
            return (-3.0, expression)
        return (1.0 / (mse + 1e-6), expression)  # Avoid division by zero
    except Exception as e:
        return (-2.0, expression)  # Return a low fitness for invalid expressions
    
def fitness2(expression):
    try:
        predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
        dif_squared_arr = []
        for i in range(len(y_values) - 1):
            if predicted_y[i] > 10000000000:
                return (-1.0, expression)
            predicted_dif = predicted_y[i + 1] - predicted_y[i]
            actual_dif    = y_values[i + 1] - y_values[i]
            dif_squared = np.power((predicted_dif - actual_dif), 2)
            dif_squared_arr.append(dif_squared)
        mse = np.mean(np.array(dif_squared_arr))
        if mse > 10000000000:
            return (-3.0, expression)
        return (1.0 / (mse + 1e-6), expression)  # Avoid division by zero
    except Exception as e:
        return (-2.0, expression)  # Return a low fitness for invalid expressions

population = []
population += [generate_random_tree(max_base_population_tree_height) for _ in range(population_size)]
if debugging_mode:
    print("Initial population: ", end="")
    print_expressions(population)

for generation in range(max_generations):
    
    if debugging_mode:
        print("Generacija: " + str(generation))
    
    all_mutation_rates.append(mutation_rate)
    
    fitness_scores1 = [fitness1(individual) for individual in population]
    fitness_scores2 = [fitness2(individual) for individual in population]
    
    fitness_scores = []
    for i in range(len(fitness_scores1)):
        new_x = (fitness_weight * fitness_scores1[i][0] + (1 - fitness_weight) * fitness_scores2[i][0], fitness_scores2[i][1])
        fitness_scores.append(new_x)

    selected_parents = sorted(fitness_scores, key=lambda x: x[0], reverse=True)[:number_of_parents]
    selected_parents = list(set(selected_parents))
    
    print("Best current expression: ", end="")
    print(str(selected_parents[0][0]) + ", ", end="")
    print_expression(selected_parents[0][1])
    
    for i in range(len(all_best_fitness_scores)):
        if i > 10:
            break
        if selected_parents[0][0] == all_best_fitness_scores[-i]:
            if mutation_rate + 0.03 <= 1:
                mutation_rate = mutation_rate + 0.03                
        else:
            mutation_rate = mutation_rate - 0.03
        if mutation_rate > 0.7:
            fresh_parents_to_add += 1
    all_best_fitness_scores.append(fitness_scores[0][0])
    print("recent fitness scores: ", end="")
    print(all_best_fitness_scores)
                
    # if debugging_mode:
    #     print("mutation_rate = " + str(mutation_rate))

    # if debugging_mode:
    #     print("Selected parents for next generation: ", end="")
    #     print_expressions([x[1] for x in selected_parents])
    #     print("Fitness scores of selected parents: ", end="")
    #     for i in range(len(fitness_scores)):
    #         print(fitness_scores[i][0], end=", ")
    #     print()

    if selected_parents[0][0] == 1000000.0:
        population = [x[1] for x in selected_parents]
        print("Najdena predčasno!")
        break

    new_population = [t[1] for t in selected_parents]
    
    if fresh_parents_to_add > 0:
        print("Fresh parents to add: " + str(fresh_parents_to_add))
    
    for i in range(fresh_parents_to_add):
        new_population.append(generate_random_tree(1))
        fresh_parents_to_add = 0
        
    if debugging_mode:
        print("Selected parents for next generation: ", end="")
        print_expressions(new_population)

    i = 0
    while len(new_population) < population_size:

        child = tree_copy(new_population[i])
        
        child = mutate(child, mutation_rate)

        new_population.append(child)

        if i + 1 == number_of_parents:
            i = 0
        else:
            i += 1
            
    # if debugging_mode:
    #     print("Nova populacija: ", end="")
    #     print_expressions(new_population)

    population = new_population

best_individual = population[0]

print("Best Equation:")
print_expression(best_individual)
print("Correct equation:")
print(correct_solution)

plt.plot(range(len(all_mutation_rates)), all_mutation_rates)
plt.show()

plt.plot(range(len(all_best_fitness_scores)), all_best_fitness_scores)
plt.show()