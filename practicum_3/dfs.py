import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_recursive(G: nx.Graph, node: Any, visited: dict[Any]):
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def dfs_iterative(G: nx.Graph, node: Any):
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def dfs_recursive_postorder(G: nx.DiGraph, node: Any, visited: dict[Any]):
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("practicum_3/graph_2.edgelist", create_using=nx.Graph)
    # plot_graph(G)

    # 1. Recursive DFS. Trivial to implement, but it does not scale on large graphs
    # In the debug mode, look at the call stack
    print("Recursive DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_recursive(G, node="0", visited=visited)
    print()

    # 2. Iterative DFS. Makes use of LIFO/stack data structure, does scale on large graphs
    print("Iterative DFS")
    print("-" * 32)
    dfs_iterative(G, node="0")
    print()

    # 3. Postorder recursive DFS for topological sort
    # If a directed graph represent tasks to be done, the topological sort tells
    # us what the task order should be, i.e. scheduling
    # Postorder DFS outputs the reversed order!
    G = nx.read_edgelist("practicum_3/graph_2.edgelist", create_using=nx.DiGraph)
    plot_graph(G)
    print("Postorder recursive DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_recursive_postorder(G, node="0", visited=visited)
