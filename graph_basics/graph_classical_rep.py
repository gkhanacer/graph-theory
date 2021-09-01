
# CLASSICAL REP.
# G = (V, E)
from collections import namedtuple
from itertools import combinations
from typing import Tuple
from pyvis.network import Network
from pprint import pprint #print 2D list
Graph = namedtuple("Graph", ["nodes", "edges", "is_directed"])

"""nodes =  ["A", "B", "C", "D"]

edges =  [
    ("A", "B"),
    ("A", "B"),
    ("A", "C"),
    ("A", "C"),
    ("A", "D"),
    ("B", "D"),
    ("C", "D"),
]"""


def _validate_num_nodes(num_nodes):
    """
    Check whether or not `num_nodes` is a 
    positive integer, and raise a Type Error 
    or Value error if it is not.
    """
    if not isinstance(num_nodes, int):
        raise TypeError("num_nodes must be integer: {}".format(type(num_nodes)))
    if num_nodes < 1:
        raise ValueError(f"number of nodes must be positive: {num_nodes=}")

# ADJACENCY LIST REP
def adjacency_dict(graph: Graph):
    """
    Returns the adjacency list representation 
    of graph node have to be hashable type. 
    Immutable. string, int, tuples immutable. 
    But dict, class, list are mutable, so they are not hashable. 
    They cannot be nodes in this graph. 
    """
    
    adj = {node: [] for node in graph.nodes}
    
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1].append(node2)
        if not graph.is_directed:
            adj[node2].append(node1)
    
    return adj


# ADJACENCY MATRIX REP.
def adjacency_matrix(graph: Graph):
    """
    Returns the adjacency matrix reptrestntation.

    Assume that graph.nodes is equivalent to range(len(graph.nodes))
    """

    adj = [[0 for node in graph.nodes] for node in graph.nodes]
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1][node2] += 1
        if not graph.is_directed:
            adj[node2][node1] += 1

    return adj

# PATH GRAPH
def path_graph(num_nodes, is_directed=False):
    """
    Returns a Graph instance representing and 
    path in `num_nodes` nodes. 
    Pn: path graph, n: number of nodes
    """
    _validate_num_nodes(num_nodes)
    nodes = range(num_nodes)
    edges = [(n, n+1) for n in range(num_nodes - 1)] # [(0,1), (1,2), ... (n-2, n-1)]
    return Graph(nodes, edges, is_directed)


# CYCLE GRAPH
def cycle_graph(num_nodes, is_directed=False):
    """
    Returns a Graph instance representing and 
    path in `num_nodes` nodes. 
    Cn: cycle graph, n: number of nodes
    """
    base_path = path_graph(num_nodes, is_directed=is_directed)
    base_path.edges.append((num_nodes-1, 0))
    return base_path

# COMPLETE GRAPH
def complete_graph(num_nodes):
    """
    Returns a Graph instance representing and 
    complete graph on  `num_nodes` nodes. 
    Kn: complete graph, n: number of nodes
    """
    _validate_num_nodes(num_nodes)
    nodes = range(num_nodes)
    edges = list(combinations(nodes, 2))
    return Graph(nodes, edges, is_directed=False)

def star_graph(num_nodes):
    """
    Returns a Graph instance representing and 
    star graph on  `num_nodes` nodes. 
    Sn: complete graph, n: number of nodes
    """
    _validate_num_nodes(num_nodes)
    nodes = range(num_nodes)
    edges = [(0, i) for i in range(1, num_nodes)]
    return Graph(nodes, edges, is_directed=False)

# VISUALIZE GRAPH
def show(graph: Graph, filename: str):
    """
    Saves an HTML file locally containing a
    visualization of the graph and returns 
    a pyvis Network instance of the graph.
    """
    net = Network(directed=graph.is_directed)
    net.add_nodes(graph.nodes)
    net.add_edges(graph.edges)
    net.show(filename)
    return net


nodes =  range(4)
edges =  [
    (0, 1),
    (0, 1),
    (0, 2),
    (0, 2),
    (0, 3),
    (1, 3),
    (2, 3),
]
G = Graph(nodes=nodes, edges=edges, is_directed=False)
adjacency_list = adjacency_dict(G)
print(adjacency_list)
adj_matrix = adjacency_matrix(G)
pprint(adj_matrix)
print(adj_matrix)

GG = Graph(nodes=range(3), edges=[(1,0), (1,2), (0,2), (2,0), (0,0)], is_directed=True)
adj_list = adjacency_dict(GG)
print(adj_list)
adj_matrix = adjacency_matrix(GG)
print(adj_matrix)

path = path_graph(num_nodes=6, is_directed=True)
cycle = cycle_graph(num_nodes=6, is_directed=True)
complete = complete_graph(num_nodes=6)
star = star_graph(num_nodes=6)
"""show(path, "path.html")
show(G, "G.html")
show(GG, "GG.html")"""

