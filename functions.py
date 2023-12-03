import random
import numpy as np
import math
import copy
from copy import deepcopy
from sympy import sympify, simplify

complex_expressions = False
invalid_expression = False # Flag for invalid expressions (dividing with 0, complex numbers, negative value in log...)

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
operators = ['+', '-', '*', '/', '**'] # Operators with both left and right child
operatorsC = ['log'] # Complex operators (log: left - expression, right - base)
trigonometric = ['sin', 'cos'] # Trigonometric operators, only have left child

class TreeNode:
    def __init__(self, value):
        self.value = str(value)
        self.left = None
        self.right = None
        
    def __eq__(self, other):
        # Check if both nodes are None (base case)
        if self is None and other is None:
            return True
        # Check if one node is None and the other is not (different structure)
        if (self is None and other is not None) or (self is not None and other is None):
            return False
        # Compare values and recursively compare left and right subtrees
        return (
            self.value == other.value and
            self.left == other.left and
            self.right == other.right
        )
    
    def __hash__(self):
        # Convert the tree structure into a hashable representation (tuple)
        return hash((self.value, self.left, self.right))

def is_operator(char):
    return char in operators

def is_operatorC(char):
    return char in operatorsC + trigonometric

def is_operand(char):
    return char in digits

def log_with_base(x, base):
    global invalid_expression
    if math.log(base) == 0:
        invalid_expression = True
        return 0
    if x <= 0:
        invalid_expression = True
        return 0
    return math.log(x) / math.log(base)

def generate_random_tree(max_height, depth=0):
    global complex_expressions
    if random.random() < (1 / max_height) * depth:
        if random.choice([True, False]):
            return TreeNode(random.choice(digits))
        else:
            if complex_expressions:
                return TreeNode(random.choice(['x', 'e']))
            else:
                return TreeNode('x')
    if complex_expressions:
        operator = random.choice(operators + operatorsC + trigonometric)
        node = TreeNode(operator)
        node.left = generate_random_tree(max_height, depth + 1)
        if operator == '**' and node.left.value == '1':
            node.left.value = random.choice(digits[1:])
        if operator == 'log':
            node.right = TreeNode(random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'e']))
        elif operator != 'sin' and operator != 'cos':
            node.right = generate_random_tree(max_height, depth + 1)
            if node.left.value in digits + ['x', 'e'] and node.right.value in digits + ['x', 'e']:
                if node.value in '+*':
                    node.left.value = 'x'
                    node.right.value = random.choice(digits)
                elif node.value in '-/':
                    if random.choice([True, False]):
                        node.left.value = random.choice(['x', 'e'])
                        node.right.value = random.choice(digits)
                    else:
                        node.left.value = random.choice(digits)
                        node.right.value = random.choice(['x', 'e'])
                elif node.value == '**' and node.left.value in digits and node.right.value in digits:
                    node.right.value = random.choice(['x', 'e'])
        return node
    else:
        operator = random.choice(operators)
        node = TreeNode(operator)
        node.left = generate_random_tree(max_height, depth + 1)
        if operator == '**':
            if node.left.value in digits:
                node.left.value = 'x'
            node.right = TreeNode(random.choice(digits))
        else:
            node.right = generate_random_tree(max_height, depth + 1)
        if node.left.value.isalnum() and node.right.value.isalnum():
            if node.value in '+*':
                node.left.value = 'x'
                node.right.value = random.choice(digits)
            elif node.value in '-/':
                if random.choice([True, False]):
                    node.left.value = 'x'
                    node.right.value = random.choice(digits)
                else:
                    node.left.value = random.choice(digits)
                    node.right.value = 'x'
        return node

def generate_trees(n, height):
    global invalid_expression
    trees = [TreeNode(None) for _ in range(n)]
    for i in range(n):
        invalid_expression = False
        trees[i] = generate_random_tree(height)
    return trees

def print_tree(root, level=0, prefix=""):
    if level == 0:
        print(prefix + str(root.value))
    else:
        print(" " * (level * 3) + prefix + str(root.value))
    if root.left is not None:
        print_tree(root.left, level + 1, "L: ")
    if root.right is not None:
        print_tree(root.right, level + 1, "R: ")

def print_expressions(arr, new = True):
    if new:
        print("[", end="")
    print("\"", end="")
    print_expression_rec(arr[0])
    print("\"", end="")
    if len(arr) > 1:
        print(", ", end="")
        print_expressions(arr[1:], False)
    else:
        print("]")

def print_expression(node):
    print_expression_rec(node)
    print()

def print_expression_rec(node):
    if complex_expressions and node is not None:
        if node.value == 'sin' or node.value == 'cos':
            print(node.value, end="(")
            print_expression_rec(node.left)
            print(")", end="")
        elif node.value == 'log':
            print_expression_rec(node.right)
            print(node.value, end="(")
            print_expression_rec(node.left)
            print(")", end="")
        elif is_operator(node.value):
            print("(", end="")
            print_expression_rec(node.left)
            print(node.value, end="")
            print_expression_rec(node.right)
            print(")", end="")
        else:
            print(node.value, end="")
    elif node is not None:
        if is_operator(node.value):
            print("(", end="")
            print_expression_rec(node.left)
            print(node.value, end="")
            print_expression_rec(node.right)
            print(")", end="")
        else:
            print(node.value, end="")

def evaluate(node, x):
    global invalid_expression
    global complex_expressions
    if invalid_expression:
        invalid_expression = False
        return 0
    
    if node.left != None and node.right != None:
        if node.value == "**" and (node.left.value == "**" or node.right.value == "**"):
            return 0.0
    
    if node != None:
        if node.value in digits + ['x', 'e', '10']:
            if node.value == 'x':
                return x
            elif complex_expressions and node.value == 'e':
                return np.e
            return int(node.value)
        elif is_operator(node.value):
            if node.value == '+':
                return evaluate(node.left, x) + evaluate(node.right, x)
            elif node.value == '-':
                return evaluate(node.left, x) - evaluate(node.right, x)
            elif node.value == '*':
                return evaluate(node.left, x) * evaluate(node.right, x)
            elif node.value == '/':
                right = evaluate(node.right, x)
                if right == 0:
                    return 0
                return evaluate(node.left, x) / right
            elif node.value == '**':
                base = evaluate(node.left, x)
                if base < 0:
                    invalid_expression = True
                    return 0
                return base ** evaluate(node.right, x)
        elif is_operatorC(node.value):
            if node.value == 'log':
                base = evaluate(node.right, x)
                if base <= 0:
                    return 0
                return log_with_base(evaluate(node.left, x), base)
            elif node.value == 'sin':
                angle = math.radians(evaluate(node.left, x))
                return math.sin(angle)
            elif node.value == 'cos':
                angle = math.radians(evaluate(node.left, x))
                return math.cos(angle)
    return None

def generate_operation(node):
    if complex_expressions:
        operator = random.choice(operators + operatorsC + trigonometric)
        if operator in trigonometric:
            node.left = TreeNode(node.value)
            node.right = None
        else:
            if node.value in digits:
                if random.choice([True, False]) or operator == 'log':
                    node.left = TreeNode(random.choice(['x', 'e']))
                    node.right = TreeNode(node.value)
                    if operator == 'log' and node.right.value == '1':
                        node.right.value = '2'
                else:
                    node.left = TreeNode(node.value)
                    node.right = TreeNode(random.choice(['x', 'e']))
            else:
                if random.choice([True, False]) or operator == 'log':
                    node.left = TreeNode(node.value)
                    if operator == 'log':
                        node.right = TreeNode(random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'e']))
                    else:
                        node.right = TreeNode(random.choice(digits))
                else:
                    node.left = TreeNode(random.choice(digits))
                    node.right = TreeNode(node.value)
    else:
        operator = random.choice(operators)
        if node.value in digits:
            if random.choice([True, False]) or operator == '**':
                node.left = TreeNode('x')
                node.right = TreeNode(node.value)
            else:
                node.left = TreeNode(node.value)
                node.right = TreeNode('x')
        else:
            if random.choice([True, False]) or operator == '**':
                node.left = TreeNode('x')
                node.right = TreeNode(random.choice(digits))
            else:
                node.left = TreeNode(random.choice(digits))
                node.right = TreeNode('x')
    node.value = operator
    return node

def mutate(root, mutation_rate):

    # print("Pred mutacijo: ")
    # print_expression(root)
    nodes_array = nodes_to_array(root)
    nodes_mutated = []
    if random.random() < mutation_rate:
        number_of_x = number_of_x_values(nodes_array)
        if number_of_x == len(nodes_array):
            mutation_type = random.choice(["change_operator", "add_operation", "remove_operation"])
        elif number_of_x >= 2:
            mutation_type = random.choice(["change_operator", "change_operand", "add_operation"])
        elif len(nodes_array) == 1:
            mutation_type = random.choice(["add_operation"])
        else:
            mutation_type = random.choice(["change_operator", "change_operand", "add_operation", "remove_operation"])
        # Filter nodes array based on mutation_type (example: if changing the operator, the selected node has to be operator => filter array to only include operator nodes)
        nodes_array_filtered = [x for x in nodes_array if
                        x not in nodes_mutated and
                        mutation_type == "change_operator" and is_operator(x.value) or
                        mutation_type == "change_operand" and is_operand(x.value) or
                        mutation_type == "add_operation" and (is_operand(x.value) or x.value == "x") or
                        mutation_type == "remove_operation" and is_operator(x.value) and (((x.left == None) or (x.left != None and x.left.left == None)) and ((x.right == None) or (x.right != None and x.right.right == None)))
                       ]
        if len(nodes_array_filtered) > 0:
            random_node = random.choice(nodes_array_filtered)
            if mutation_type == "change_operator":
                if random_node.value == 'sin':
                    random_node.value = 'cos'
                elif random_node.value == 'cos':
                    random_node.value = 'sin'
                elif random_node.value != 'log':
                    random_node.value = random.choice([x for x in operators if x != random_node.value])
            if mutation_type == "change_operand":
                random_node.value = random.choice([x for x in digits if x != random_node.value])
            if mutation_type == "add_operation":
                random_operation = generate_operation(random_node)
                random_node.value = random_operation.value
                random_node.left = random_operation.left
                random_node.right = random_operation.right
            if mutation_type== "remove_operation": # tuki je treba nardit se da bo nov value x alpa digit glede na to a je na drugi strani enacbe x alpa digit (bi rabl mogoce node.parent)
                random_node.value = random.choice([random_node.left.value, random_node.right.value])
                random_node.left = None
                random_node.right = None
            
            nodes_mutated.append(random_node)

    # print("Po: ")
    # print_expression(root)
    if number_of_x_values(nodes_to_array(root)) == 0:
        # return mutate(root, mutation_rate)
        invalid_expression = True
    return root

def tree_copy(root):
    if root is None:
        return None

    new_root = TreeNode(root.value)
    new_root.left = tree_copy(root.left)
    new_root.right = tree_copy(root.right)

    return new_root

def number_of_x_values(arr):
    return len([x for x in arr if x.value == "x"])

def nodes_to_array(root):
    def in_order_traversal(node, result):
        if node is not None:
            in_order_traversal(node.left, result)
            result.append(node)
            in_order_traversal(node.right, result)

    result = []
    in_order_traversal(root, result)
    return result

def flatten_tree(node):
    if node is None:
        return []
    return flatten_tree(node.left) + [node] + flatten_tree(node.right)

def crossover(parent1, parent2):
    # Create deep copies of the parents to avoid modifying them directly
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # Select a non-root node from parent1
    parent1_node = get_random_non_root_node(parent1)
    # Select a non-root node from parent2
    parent2_node = get_random_non_root_node(parent2)

    # Swap the selected nodes and their descendants
    swap_nodes(child1, parent1_node, parent2_node)

    # Swap the selected nodes and their descendants in the second child
    swap_nodes(child2, parent2_node, parent1_node)

    return child1, child2

def get_random_non_root_node(tree):
    # Get a list of all non-root nodes in the tree
    non_root_nodes = get_non_root_nodes(tree)

    # Select a random non-root node
    return random.choice(non_root_nodes)

def get_non_root_nodes(node):
    # Helper function to get a list of all non-root nodes in the tree
    non_root_nodes = []
    if node.left:
        non_root_nodes.append(node.left)
        non_root_nodes.extend(get_non_root_nodes(node.left))
    if node.right:
        non_root_nodes.append(node.right)
        non_root_nodes.extend(get_non_root_nodes(node.right))
    return non_root_nodes

def swap_nodes(tree, node1, node2):
    # Helper function to swap two nodes and their descendants in the tree
    if tree is None:
        return

    if tree == node1:
        # Replace node1 with a deep copy of node2
        tree.value = node2.value
        tree.left = copy.deepcopy(node2.left)
        tree.right = copy.deepcopy(node2.right)
    else:
        # Recursively swap nodes in the left and right subtrees
        swap_nodes(tree.left, node1, node2)
        swap_nodes(tree.right, node1, node2)

def expressionsAreRepeating(population):
    for i in range(len(population)):
        for j in range(len(population)):
            if isEqual(population[i], population[j]):
                return True   
    return False
            
def isEqual(e1, e2):
    if e1 == None and e2 == None:
        return True
    if (e1.value != e2.value):
        return False
    return isEqual(e1.left, e2.left) and isEqual(e1.right, e2.right)

def uniqueExpressions(population):
    expressions = [x[1] for x in population]
    for i in range(len(expressions)):
        for j in range(len(expressions)):
            if isEqual(expressions[i], expressions[j]):
                del population[j]
                return uniqueExpressions(population)
    return population


def expression_to_string_rec(node):
    result = ""
    if complex_expressions and node is not None:
        if node.value == 'sin' or node.value == 'cos':
            result += node.value + "("
            result += expression_to_string_rec(node.left)
            result += ")"
        elif node.value == 'log':
            result += "log("
            result += expression_to_string_rec(node.left)
            result += ", "
            result += expression_to_string_rec(node.right)
            result += ")"
        elif is_operator(node.value):
            result += "("
            result += expression_to_string_rec(node.left)
            result += node.value
            result += expression_to_string_rec(node.right)
            result += ")"
        else:
            result += node.value
    elif node is not None:
        if is_operator(node.value):
            result += "("
            result += expression_to_string_rec(node.left)
            result += node.value
            result += expression_to_string_rec(node.right)
            result += ")"
        else:
            result += node.value
    return result

def simplify_tree(tree_to_simp):
    s = expression_to_string_rec(tree_to_simp)
    simp = sympify(s)
    simp1 = simplify(simp)
    print("Normal expression", s)
    print("Simplified expression:", simp1)


tree11 = generate_random_tree(5)
simplify_tree(tree11)


""" tree = generate_random_tree(3)
print_tree(tree)
print_expression_rec(tree)
print()
mutated = mutate(tree, 1)
print_tree(mutated)
print_expression_rec(mutated)
print() """

# tree1 = generate_random_tree(25)
# tree2 = tree_copy(tree1)
# population = [tree1, tree2]
# if expressionsAreRepeating(population):
#     population = population[:-1]

# print(len(population))
"""
expression = generate_random_tree(1)
x_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
print(predicted_y)
"""

""" tree1 = generate_random_tree(5)
tree2 = generate_random_tree(5)
arrT1 = nodes_to_array(tree1)
s = ""
for i in range(len(arrT1)):
    s += str(arrT1[i].value)
print(s)
simp = sympify(s)
simp1 = simplify(simp)
print_expression_rec(tree1)
print()
print("Simplified expression:", simp1) """

"""
tree1 = generate_random_tree(3)
tree2 = generate_random_tree(3)
chld1, chld2 = crossover(tree1, tree2)

print_tree(tree1)
print_expression_rec(tree1)
print()
print_tree(tree2)
print_expression_rec(tree2)
print()
print_tree(chld1)
print_expression_rec(chld1)
print()
print_tree(chld2)
print_expression_rec(chld2)"""
