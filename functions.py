import random
import numpy as np
import math
from copy import deepcopy

complex_expressions = True
invalid_expression = False # Flag for invalid expressions (dividing with 0, complex numbers...)

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
operators = ['+', '-', '*', '/', '**'] # Operators with both left and right child
operatorsC = ['log'] # Complex operators (log: left - expression, right - base)
trigonometric = ['sin', 'cos'] # Trigonometric operators, only have left child

class TreeNode:
    def __init__(self, value):
        self.value = str(value)
        self.left = None
        self.right = None

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
        return 0
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

def mutate(root, mutation_rate):

    # print("Pred mutacijo: ")
    # print_expression(root)
    nodes_array = nodes_to_array(root)
    nodes_mutated = []
    for i in range(mutation_rate):
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
                random_node.value = random.choice([x for x in operators if x != random_node.value])
            if mutation_type == "change_operand":
                random_node.value = random.choice([x for x in digits if x != random_node.value])
            if mutation_type == "add_operation":
                random_operation = generate_random_tree(1)
                random_node.value = random_operation.value
                # mogoce lahko implementiramo da vzame value ki je bil prej na tem mestu:
                # npr. iz "3" bi potem lahko dobili samo "x + 3", ker zdaj lahko dobimo tudi karkoli drugega npr. "x * 4" kar nima vec veze s "3"
                random_node.left = random_operation.left
                random_node.right = random_operation.right
            if mutation_type== "remove_operation": # tuki je treba nardit se da bo nov value x alpa digit glede na to a je na drugi strani enacbe x alpa digit (bi rabl mogoce node.parent)
                random_node.value = random.choice(digits + ["x"])
                random_node.left = None
                random_node.right = None
            
            nodes_mutated.append(random_node)

    # print("Po: ")
    # print_expression(root)
    if number_of_x_values(nodes_to_array(root)) == 0:
        return mutate(root, mutation_rate)
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

tree = generate_random_tree(10)
#print_expression(tree)
def flatten_tree(node):
    if node is None:
        return []
    return flatten_tree(node.left) + [node] + flatten_tree(node.right)

def crossover(parent1, parent2):
    flat_parent1 = flatten_tree(parent1)
    flat_parent2 = flatten_tree(parent2)

    # Determine the crossover point (random index between 30% and 70% of the shorter array)
    min_length = min(len(flat_parent1), len(flat_parent2))
    crossover_point = random.randint(min_length * 3 // 10, min_length * 7 // 10)
    print("CROSSOVER POINT___", crossover_point)

    # Create a set to keep track of unique values in the child tree
    unique_values = set()

    # Create an array of nodes by combining nodes from parent1 up to the crossover point and parent2 after the crossover point
    child_nodes = []

    if crossover_point < len(flat_parent1):
        for node in flat_parent1[:crossover_point + 1]:
            if node.value not in unique_values:
                child_nodes.append(node)
                unique_values.add(node.value)

    if crossover_point < len(flat_parent2):
        for node in flat_parent2[crossover_point + 1:]:
            if node.value not in unique_values:
                child_nodes.append(node)
                unique_values.add(node.value)

    # Construct the child tree from the array of nodes
    child_tree = construct_tree_from_nodes(child_nodes)

    return child_tree

def construct_tree_from_nodes(nodes):
    if not nodes:
        return None

    root = clone_tree(nodes[0])
    current_node = root

    for node in nodes[1:]:
        current_node.right = clone_tree(node)
        current_node = current_node.right

    return root

def clone_tree(node):
    if node is None:
        return None

    new_node = TreeNode(node.value)
    new_node.left = clone_tree(node.left)
    new_node.right = clone_tree(node.right)

    return new_node

tree = generate_random_tree(5)
print_tree(tree)
print_expression_rec(tree)
print(evaluate(tree, 10))
# tree1 = generate_random_tree(5)
# tree2 = generate_random_tree(5)
# chld1 = crossover(tree1, tree2)
#print_tree(tree)
# print_expression(tree1)
# print_expression(tree2)
# print_expression(chld1)

#print(evaluate(tree, 1))