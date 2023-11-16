import numpy as np
import pandas as pd
import pygad
import matplotlib.pyplot as plt
import sympy as sp
from functions import *

# Define the input-output pairs (x, y)
x = np.array([1, 2, 3])
y = np.array([2, 4, 6])

# Task 2 (Mark Mihelič)
def fitness_function(ga_instance, solution, solution_idx):

    expression = f"lambda x: {solution}"
    print(expression)
    try:
        function = eval(expression)
        predicted_y = [function(xi) for xi in x]
        mse = np.mean((np.array(predicted_y) - y) ** 2)
        return 1.0 / (mse + 1e-6)  # Avoid division by zero
    except Exception as e:
        return 0.0  # Return a low fitness for invalid expressions

# Create an instance of the pygad.GA class
ga = pygad.GA(num_generations=50, 
             num_parents_mating=10, 
             fitness_func=fitness_function, 
             sol_per_pop=20, 
             num_genes=len("a*x"))

# Run the genetic algorithm
ga.run()

df = pd.read_csv("data.txt").head()
print(df)

# Define a function to parse expressions and build expression trees
def parse_expression(expression_str):
    try:
        # Use sympy to parse the expression
        parsed_expression = sp.sympify(expression_str)
        return parsed_expression
    except sp.SympifyError as e:
        print(f"Error parsing expression: {expression_str}")
        return None
    
    

    
# Apply the parsing function to the "Equation" column and store the results in a new column
# df['Expression'] = df['Equation'].apply(parse_expression)

# Get the best solution found by the genetic algorithm
best_solution = ga.best_solution()
print(best_solution)


# print("main branch zacni delat")
print("Raztegnu ti bokm supak")