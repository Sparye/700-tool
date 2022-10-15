from ff_util import get_func_calls
import ast
import astor
def get_node(callName,tree):
    node_list = []
    func_calls, args = get_func_calls(callName,tree)
    for i in range(len(func_calls)):
        node_list.append(func_calls[i])
    return node_list[0]

def has_node(callName,tree):
    node_list = []
    func_calls, args = get_func_calls(callName,tree)
    for i in range(len(func_calls)):
        node_list.append(func_calls[i])
    return len(node_list) != 0

def has_validation_split(tree):
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Attribute) and (node.func.attr=="fit"):
                args = []
                for keyword in node.keywords:
                    args.append(keyword.arg)
                if not "validation_split" in args:
                    print("adding validation split to function")
                    return False
    return True

def add_validation_split(tree):
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Attribute) and (node.func.attr=="fit"):
                node.keywords.append(ast.keyword(arg="validation_split",value=ast.Num(n=0.2)))
    return tree            

def get_model_name(tree):
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Attribute) and (node.func.attr=="fit"):
                if isinstance(node.func.value,ast.Name):
                    return node.func.value.id

def load_tree(input_file):
    tree = astor.code_to_ast.parse_file(input_file)
    return tree