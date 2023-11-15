class TreeNode:
    def __init__(self, value):
        self.value = str(value)
        self.left = None
        self.right = None

def is_operator(char):
    operators = ['+', '-', '*', '/', '**']
    return char in operators

def create_expression_tree(expression):
    stack = []
    i = 0

    while i < len(expression):
        if expression[i] == '(':
            stack.append(expression[i])
            i += 1
        elif expression[i] == ')':
            right_operand = stack.pop()
            operator = stack.pop()
            left_operand = stack.pop()
            node = TreeNode(operator)
            node.left = left_operand
            node.right = right_operand
            stack.pop() # Remove the opening parenthesis
            stack.append(node)
            i += 1
        elif expression[i].isalnum():
            start = i
            while i < len(expression) and (expression[i].isalnum() or expression[i] == '.'):
                i += 1
            operand = TreeNode(expression[start:i])
            stack.append(operand)
        elif is_operator(expression[i]):
            # while (stack and is_operator(stack[-1]) and
            #        (expression[i] in '+-' or expression[i] in '*/' and stack[-1] in '*/' or
            #         expression[i] == '^' and stack[-1] == '^' and expression[i] != stack[-1])):
            if (expression[i] == '*' and expression[i+1] == '*'):
                operator = stack.append("**")
                i += 2
            else:
                operator = stack.append(expression[i])
                i += 1
        elif expression[i] == ' ':
            i += 1
        else:
            raise ValueError("Invalid character in the expression")

    while len(stack) > 1:
        operator = stack.pop()
        right_operand = stack.pop()
        left_operand = stack.pop()
        node = TreeNode(operator)
        node.left = left_operand
        node.right = right_operand
        stack.append(node)

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]

def print_tree(root, level=0, prefix=""):
    if isinstance(root, TreeNode):
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

tree = create_expression_tree('((x+2)*3)')
print_tree(tree)
result = evaluate(tree, 2)
print(result)
