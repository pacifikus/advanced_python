import ast
import inspect
import uuid
from collections import deque
from math import sqrt

import astunparse
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

ast_literals = ['Constant', 'List']
ast_math = ['Add', 'Sub', 'sqrt', 'Pow', 'Mult', 'Div']
ast_expressions = [
    'Compare', 'Expr', 'Call', 'BinOp', 'Add', 'Eq', 'Sub', 'Subscript',
    'UnaryOp', 'USub', 'Index', 'Attribute', 'For', 'Return'
]
ast_statements = ['Assign']
ast_functions = ['fib', 'return', 'arg', 'n', 'fib_num', 'i', 'result']


def fib(n):
    result = []
    for i in range(n):
        fib_num = (((1 + sqrt(5)) ** n) - (1 - sqrt(5)) ** n) / (2 ** n * sqrt(5))
        result.append(fib_num)
    return result


def get_node_label(node):
    if type(node) == ast.arguments:
        label = ', '.join([item.arg for item in node.args])
    elif type(node) in [ast.Compare, ast.Name]:
        label = astunparse.unparse(node).replace("\n", "")
    elif type(node) == ast.Attribute:
        label = astunparse.unparse(node).replace("\n", "").replace(".", ".\n")
    elif type(node) == ast.Constant:
        label = node.__class__.__name__ + "\n" + astunparse.unparse(
            node,
        ).replace("\n", "")
    elif hasattr(node, 'name'):
        label = node.name
    else:
        label = node.__class__.__name__
    return label.replace(':', '')


def get_node_color(node_type):
    if node_type in ast_functions:
        return 'red'
    elif node_type in ast_literals:
        return 'pink'
    elif node_type in ast_math:
        return 'orange'
    return 'green'  # ast_expressions + ast_statements


def build_graph():
    fib_tree = ast.parse(inspect.getsource(fib))
    G = nx.DiGraph()
    nodes = deque()
    start = next(ast.walk(fib_tree)).body[0]
    start_id = str(uuid.uuid4())
    nodes.append((start, start_id))
    G.add_node(start_id, label=start.name)

    while len(nodes) != 0:
        cur_node, cur_node_id = nodes.pop()
        for node in ast.iter_child_nodes(cur_node):
            if type(node) in [ast.Load, ast.Store]:
                break
            node_label = get_node_label(node)
            node_id = str(uuid.uuid4())
            nodes.append((node, node_id))

            G.add_node(node_id, label=node_label)
            G.add_edge(cur_node_id, node_id)
    return G


def build_ast(G):
    options = {
        "edge_color": "tab:gray",
        "node_size": 1500,
        "node_color": "tab:green",
        "alpha": 0.9,
    }
    nx.draw(G, with_labels=True, **options)
    plt.show()


def build_ast_beauty(G):
    color_map = []

    options = {
        "edge_color": "tab:gray",
        "node_size": 3000,
    }
    pos = graphviz_layout(G, prog="dot")
    labels_dict = {}
    for node in G.nodes(data=True):
        labels_dict[node[0]] = node[1]['label']
        color_map.append(get_node_color(node[1]['label'].split('\n')[0]))
    nx.draw(
        G,
        pos,
        labels=labels_dict,
        with_labels=True,
        node_color=color_map,
        **options,
    )
    plt.show()


graph = build_graph()
# build_ast(graph) # medium task
build_ast_beauty(graph)  # hard task
