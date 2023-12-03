import random
import numpy as np
import math
from copy import deepcopy

complex_expressions = False
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
        if operator == 'log':
            node.right = TreeNode(random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'e']))
        if operator != 'sin' and operator != 'cos':
            node.right = generate_random_tree(max_height, depth + 1)
            if node.left.value.isalnum() and node.right.value.isalnum():
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
        return node
    else:
        operator = random.choice(operators)
        node = TreeNode(operator)
        node.left = generate_random_tree(max_height, depth + 1)
        if operator == '**':
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
    if node is not None:
        if node.left is not None or node.right is not None:
            if is_operator(node.value):
                if node.value in ['+', '-', '*', '/', '**']:
                    print("(", end="")
                print_expression_rec(node.left)
                print(node.value, end="")
                print_expression_rec(node.right)
                if node.value in ['+', '-', '*', '/', '**']:
                    print(")", end="")
            else:
                print_expression_rec(node.left)
                print(node.value, end="")
                print_expression_rec(node.right)
        else:
            print(node.value, end="")

def evaluate(node, x):
    global invalid_expression
    global complex_expressions
    if invalid_expression:
        invalid_expression = False
        return 0
    if node != None:
        if node.value in digits + ['x', 'e']:
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

# tree = generate_random_tree(10)
# print_expression(tree)
# def is_operand(node):
#     return node.value.isdigit() or node.value in {'+', '-', '*', '**', '/'}

def crossover(parent1, parent2):
    # Create deep copies of the parents to avoid modifying them directly
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    operators_extended = ['+', '-', '*', '/', '**', 'log', 'sin', 'cos']
    # Select a non-root node from parent1
    parent1_node = get_random_non_root_node_with_operator(parent1,operators_extended)
    # Select a non-root node from parent2
    parent2_node = get_random_non_root_node_with_operator(parent2,operators_extended)

    # Swap subtrees between the two parents at the crossover points
    swap_subtrees(child1, crossover_point1, parent2, crossover_point2)
    swap_subtrees(child2, crossover_point2, parent1, crossover_point1)

    return child1, child2

def get_random_non_root_node_with_operator(tree, operators):
    # Get a list of all non-root nodes with values in the specified operators list
    valid_nodes = get_valid_nodes(tree, operators)

    # Select a random node from the valid nodes
    return random.choice(valid_nodes)

def get_valid_nodes(node, operators):
    # Helper function to get a list of all non-root nodes with values in the specified operators list
    valid_nodes = []
    if node and node.value in operators:
        valid_nodes.append(node)
    if node.left:
        valid_nodes.extend(get_valid_nodes(node.left, operators))
    if node.right:
        valid_nodes.extend(get_valid_nodes(node.right, operators))
    return valid_nodes

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

# tree1 = generate_random_tree(25)
# tree2 = tree_copy(tree1)
# population = [tree1, tree2]
# if expressionsAreRepeating(population):
#     population = population[:-1]

# print(len(population))

expression = generate_random_tree(1)
print_expression(expression)
x_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
predicted_y = [evaluate(expression, xi) for xi in x_values.tolist()]
print(predicted_y)