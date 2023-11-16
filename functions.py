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

def is_operand(char):
    return char in digits

def generate_random_tree(max_height, depth=0):
    if random.random() < (1 / max_height) * depth:
        if random.choice([True, False]):
            return TreeNode(random.choice(digits))
        else:
            return TreeNode('x')
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

def print_expression(node):
    print_expression_rec(node)
    print()

def print_expression_rec(node):
    if node is not None:
        if node.left is not None or node.right is not None:
            if is_operator(node.value):
                if node.value in ['+', '-']:
                    print("(", end="")
                print_expression_rec(node.left)
                print(node.value, end="")
                print_expression_rec(node.right)
                if node.value in ['+', '-']:
                    print(")", end="")
            else:
                print_expression_rec(node.left)
                print(node.value, end="")
                print_expression_rec(node.right)
        else:
            print(node.value, end="")

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

def mutate(root, mutation_rate):

    print_expression(root)

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
                        mutation_type == "add_operation" and is_operand(x.value) or
                        mutation_type == "remove_operation" and is_operator(x.value) and (((x.left == None) or (x.left != None and x.left.left == None)) and ((x.right == None) or (x.right != None and x.right.right == None)))
                       ]
        print(mutation_type)
        print(len(nodes_array_filtered))
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
        
    print_expression(root)

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

def nodes_to_array(root, arr = []):
    def in_order_traversal(node, result):
        if node is not None:
            in_order_traversal(node.left, result)
            result.append(node)
            in_order_traversal(node.right, result)

    result = []
    in_order_traversal(root, result)
    return result

tree = generate_random_tree(10)
print_expression(tree)