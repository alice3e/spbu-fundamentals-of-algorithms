import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_recursive(G: nx.Graph, node_name: Any, visited: dict[Any]) -> None:
    #edge_highlight = []
    visited[node_name] = True

    for neighbor in G.neighbors(node_name):
        if not visited[neighbor]:
            #edge_highlight.append((node_name,neighbor))
            #plot_graph(G,highlighted_edges=edge_highlight)
            dfs_recursive(G , neighbor , visited)
    pass


def dfs_iterative(G: nx.Graph, node_name: Any, visited: dict[Any]) -> None:
    node_highlight = []
    current = []
    current.append(node_name)

    while (current):
        current_vertex = current.pop()
        node_highlight.append(current_vertex)
        visited[current_vertex] = True
        for neighbor in nx.all_neighbors(G,current_vertex):
            if (visited[neighbor] == False and (neighbor not in current)):
                current.append(neighbor)
        plot_graph(G, highlighted_nodes=node_highlight)
    pass


def dfs_recursive_postorder(G: nx.DiGraph, node: Any, visited: dict[Any]) -> None:
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    # Load and plot the graph
    #G = nx.erdos_renyi_graph(n=15, p=0.2)  # кол-во узлов, вероятность появления связи
    G = nx.read_edgelist("graph_2.edgelist", create_using=nx.Graph)
    plot_graph(G)

    # 1. Recursive DFS. Trivial to implement, but it does not scale on large graphs
    # In the debug mode, look at the call stack
    print()
    print("Recursive DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_iterative(G, node_name=list(nx.nodes(G))[0], visited=visited)

    # highlighted_edges = dfs_recursive(G, node_name="0", visited=visited)
    print(visited)
    # plot_graph(G, highlighted_edges=highlighted_edges)
    # 2. Iterative DFS. Makes use of LIFO/stack data structure, does scale on large graphs
    # print("Iterative DFS")
    # print("-" * 32)
    # dfs_iterative(G, node="0")
    # print()

    # 3. Postorder recursive DFS for topological sort
    # If a directed graph represent tasks to be done, the topological sort tells
    # us what the task order should be, i.e. scheduling
    # Postorder DFS outputs the reversed order!
    # G = nx.read_edgelist("graph_2.edgelist", create_using=nx.DiGraph)
    # plot_graph(G)
    # print("Postorder iterative DFS")
    # print("-" * 32)
    # visited = {n: False for n in G}
    # dfs_recursive_postorder(G, node="0", visited=visited)

#%%
