import random

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
operators = ['+', '-', '*', '/']

class TreeNode:
    def __init__(self, value):
        self.value = str(value)
        self.left = None
        self.right = None

def is_operator(char):
    return char in operators

def create_expression_tree(expression):
    stack = []
    i = 0

    while i < len(expression):
        if expression[i] == '(':
            stack.append(expression[i])
            i += 1
        elif expression[i] == ')':
            if len(stack) > 2:
                right_operand = stack.pop()
                operator = stack.pop()
                left_operand = stack.pop()
                stack.pop()
                node = TreeNode(operator)
                node.left = left_operand
                node.right = right_operand
                stack.append(node)
            else:
                raise ValueError("Mismatched parentheses in the expression")
            i += 1
        elif expression[i].isalnum():
            start = i
            while i < len(expression) and (expression[i].isalnum() or expression[i] == '.'):
                i += 1
            stack.append(TreeNode(expression[start:i]))
        elif is_operator(expression[i]):
            while (len(stack) > 2 and is_operator(stack[-2]) and
                    ((expression[i] in '+-' and stack[-2] in '*/') or
                    (expression[i] in '*/' and stack[-2] in '*/') or
                    (expression[i] in '+-' and stack[-2] in '+-'))):
                right_operand = stack.pop()
                operator = stack.pop()
                left_operand = stack.pop()
                node = TreeNode(operator)
                node.left = left_operand
                node.right = right_operand
                stack.append(node)
            stack.append(expression[i])
            i += 1
        elif expression[i] == ' ':
            i += 1
        else:
            raise ValueError("Invalid character in the expression")

    while len(stack) > 1:
        right_operand = stack.pop()
        operator = stack.pop()
        left_operand = stack.pop()
        node = TreeNode(operator)
        node.left = left_operand
        node.right = right_operand
        stack.append(node)

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]

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
                return evaluate(node.left, x) / evaluate(node.right, x)
            if node.value == '**':
                return evaluate(node.left, x) ** evaluate(node.right, x)
    return None

def mutate(expression_root, mutation_rate):
    if random.random() < mutation_rate:
        x = 0
    return expression_root
tree = create_expression_tree('(x+2)*3)')
print_tree(tree)
# result = evaluate(tree, 2)
# print(result)
