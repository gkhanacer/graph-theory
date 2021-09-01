#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from graph_classical_rep import adjacency_dict
from pyvis.network import Network
from cell import Cell

class Graph:

    def __init__(self):
        self.nodes = list()
        self.edges = list()
        self.cells = [Cell]
        self.is_directed = False   
        self.node_counter = 0
        
    """    def __init__(self, nodes, edges, is_directed):
        self.nodes = nodes
        self.edges = edges
        self.is_directed = is_directed
        self.graph = self.adjacency_dict()
        """

    # ADJACENCY LIST REP
    def adjacency_dict(self):
        """
        Returns the adjacency list representation 
        of graph node have to be hashable type. 
        Immutable. string, int, tuples immutable. 
        But dict, class, list are mutable, so they are not hashable. 
        They cannot be nodes in this graph. 
        """
        
        adj = {node: [] for node in self.nodes}
        
        for edge in self.edges:
            node1, node2 = edge[0], edge[1]
            adj[node1].append(node2)
            if not self.is_directed:
                adj[node2].append(node1)
        
        return adj

    # ADJACENCY MATRIX REP.
    def adjacency_matrix(self):
        """
        Returns the adjacency matrix reptrestntation.

        Assume that graph.nodes is equivalent to range(len(graph.nodes))
        """

        adj = [[0 for node in self.nodes] for node in self.nodes]
        for edge in self.edges:
            node1, node2 = edge[0], edge[1]
            adj[node1][node2] += 1
            if not self.is_directed:
                adj[node2][node1] += 1

        return adj

    def add_node(self, node, edges):
        pass

    def remove_node(self, node):
        pass

    def add_edge(self, node1, node2):
        pass

    def remove_edge(self, node1, node2):
        pass

    def next_step(self):
        pass

    def add_cell(self, cell: Cell):
        self.cells.append(cell)

    def show(self, filename):
        """
        Saves an HTML file locally containing a
        visualization of the graph and returns 
        a pyvis Network instance of the graph.
        """
        net = Network(directed=self.is_directed)
        net.add_nodes(self.nodes)
        net.add_edges(self.edges)
        net.show(filename)
        return net

def main():
    """    nodes =  range(4)
    edges =  [ (0, 1), (0, 2), (0, 3), (3, 1),  (2, 3) ]
    graph = Graph(nodes=nodes, edges=edges, is_directed=True)
    graph.show("a.html")
    """
    cell_size = 50
    start_position = (0,0)
    cell = Cell(pose=start_position, size=cell_size)
    print(cell.id)

    cell1 = Cell((0,1), cell_size)
    print(cell1.id)

    graph = Graph()
    graph.add_cell(cell=cell)
    graph.add_cell(cell=cell1)
    graph.show("a.html")



if __name__ == '__main__':
    main()