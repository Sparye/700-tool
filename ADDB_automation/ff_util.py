import ast
from collections import deque


class FuncCallVisitor(ast.NodeVisitor):
    """
    This is the AST visitor that returns the fully qualified names of all function calls
    """

    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(target, tree):
    """
    This function get all the function calls and arguments that matches a specific target
    for example 'keras.layers.Dense'

    it returns a list of all AST nodes that calls the specific targets with the list of arguments

    In Python, args is when you specify only the value, keywords is when you specify the argument name.

    For example, tf.keras.layers.Dense(12, activation='relu')

    there is on args (12)
    there is one keyword (activation='relu')
    """
    func_calls = []
    arguments = []
    for node in ast.walk(tree):  # this navigates all teh nodes in the AST
        if isinstance(node, ast.Call):
            call_visitor = FuncCallVisitor()
            call_visitor.visit(node.func)
            if call_visitor.name.endswith(target):  # check if the function call is matching the target
                func_calls.append(node)
                args = node.args
                keywords = node.keywords
                arguments.append(args + keywords)  # combines the args and keywords
    return func_calls, arguments


def get_assign_calls(target, tree):
    """
    This function looks for instances of assignment for certain variables by using their id

    returns a list of all assignments for this variable
    """
    target_assign_nodes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for targets in node.targets:
                if targets.id == target:
                    target_assign_nodes.append(node)

    return target_assign_nodes


def get_assign_nodes_using_func(target, tree):
    """
    This function searches for all nodes of ast.Assign type and then checks that the
    the nodes on the right of the assignment are of a specific function type "target"

    returns a list of all instances of this
    """
    assign_node_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr == target:
                    assign_node_list.append(node)
            if isinstance(node.value, ast.UnaryOp):
                if isinstance(node.value.operand, ast.Call):
                    if node.value.operand.func.attr == target:
                        assign_node_list.append(node)

    return assign_node_list
