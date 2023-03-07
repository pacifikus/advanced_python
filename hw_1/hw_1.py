import ast
import inspect
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


ast_literals = ['Constant', 'List']
ast_vars = ['Name', 'Load', 'Store']
ast_control_flow = ['If']
ast_expressions = [
    'Compare', 'Expr', 'Call', 'BinOp', 'Add', 'Eq', 'Sub', 'Subscript',
    'UnaryOp', 'USub', 'Index', 'Attribute',
]
ast_statements = ['Assign']
ast_functions = ['fib', 'Return', 'arg', 'n']


def fib(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        lst = fib(n - 1)
        lst.append(lst[-1] + lst[-2])
        return lst


def get_node_label(node):
    if type(node) == ast.arguments:
        label = ', '.join([item.arg for item in node.args])
    elif hasattr(node, 'name'):
        label = node.name
    else:
        label = node.__class__.__name__
    return label


def get_node_color(node_type):
    if node_type in ast_functions:
        return 'red'
    elif node_type in ast_literals + ast_vars:
        return 'pink'
    elif node_type in ast_control_flow:
        return 'orange'
    return 'green'  # ast_expressions + ast_statements


def build_graph():
    fib_tree = ast.parse(inspect.getsource(fib))
    G = nx.DiGraph()
    nodes = deque()
    start = next(ast.walk(fib_tree)).body[0]
    nodes.append(start)
    G.add_node(start.name)

    while len(nodes) != 0:
        cur_node = nodes.pop()
        for node in ast.iter_child_nodes(cur_node):
            node_label = get_node_label(node)
            cur_node_label = get_node_label(cur_node)
            G.add_node(node_label)
            G.add_edge(cur_node_label, node_label)
            nodes.append(node)
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
    color_map = [get_node_color(node) for node in G]

    options = {
        "edge_color": "tab:gray",
        "node_size": 3000,
    }
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, node_color=color_map, **options)
    plt.show()


graph = build_graph()
# build_ast(graph) # medium task
build_ast_beauty(graph)  # hard task
