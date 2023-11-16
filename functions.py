import random

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
operators = ['+', '-', '*', '/', '**']

class TreeNode:
    def __init__(self, value):
        self.value = str(value)
        self.left = None
        self.right = None

def is_operator(char):
    return char in operators

def generate_random_tree(max_height, depth=0):
    if random.random() < (1 / max_height) * depth:
        if random.choice([True, False]):
            return TreeNode(random.choice(digits))
        else:
            return TreeNode('x')
    operator = random.choice(operators)
    node = TreeNode(operator)
    node.left = generate_random_tree(max_height, depth + 1)
    node.right = generate_random_tree(max_height, depth + 1)
    if node.left.value.isalnum() and node.right.value.isalnum():
        if node.value == '**' or node.value in '+*':
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
    trees = [TreeNode(None) for _ in range(n)]
    for i in range(n):
        trees[i] = generate_random_tree(height)
    return trees

def print_tree(root, level=0, prefix=""):
    if level == 0:
        print(prefix + str(root.value))
    else:
        print(" " * (level * 3) + prefix + str(root.value))
    if root.left is not None or root.right is not None:
        print_tree(root.left, level + 1, "L: ")
        print_tree(root.right, level + 1, "R: ")

def evaluate(node, x):
    if node != None:
        if node.value.isalnum():
            if node.value == 'x':
                return x
            return int(node.value)
        if is_operator(node.value):
            if node.value == '+':
                return evaluate(node.left, x) + evaluate(node.right, x)
            if node.value == '-':
                return evaluate(node.left, x) - evaluate(node.right, x)
            if node.value == '*':
                return evaluate(node.left, x) * evaluate(node.right, x)
            if node.value == '/':
                right = evaluate(node.right, x)
                if right == 0:
                    return 0
                return evaluate(node.left, x) / right
            if node.value == '**':
                return evaluate(node.left, x) ** evaluate(node.right, x)
    return None

def mutate(expression_root, mutation_rate):
    if random.random() < mutation_rate:
        x = 0
    return expression_root

tree = generate_random_tree(5)
print_tree(tree)
# print(evaluate(tree, 1))
