import networkx as nx
from src.plotting import plot_graph
from typing import Any
import os

TEST_GRAPH_FILES = [
    "practicum_2/homework/advanced/graph_1_wo_cycles.edgelist",
    "practicum_2/homework/advanced/graph_2_wo_cycles.edgelist",
    "practicum_2/homework/advanced/graph_3_w_cycles.edgelist",
]


def get_keys(d, key_to_find):
    for key, val in d.items():
        if val == key_to_find:
            return key
        else:
            return -1


stack = []
flag = 0


# nx.simple_cycles(G)) - WONT BE USED
def has_cycles_rec(G: nx.DiGraph, starting_node, visited: dict[Any], node_highlight, edge_highlight):
    global flag
    visited[starting_node] = True
    node_highlight.append(starting_node)
    global stack, stack_copy
    stack.append(starting_node)
    for neighbor in G.successors(starting_node):
        edge_highlight.append((starting_node, neighbor))
        # plot_graph(G, highlighted_edges=edge_highlight, highlighted_nodes=node_highlight)
        if visited[neighbor]:
            #print(f'{stack} <- cycle info')
            flag = 1
            return flag
        else:
            has_cycles_rec(G, neighbor, visited, node_highlight, edge_highlight)
    node_highlight.pop(node_highlight.index(starting_node))
    visited[starting_node] = False

    stack.pop()
    return flag

def has_cycles(g: nx.DiGraph):
    visited = {n: False for n in g}  # False - not visited, True - visited
    nodes_to_highlight = []
    edges_to_highlight = []
    flag_cycles = has_cycles_rec(g, get_keys(visited, False), visited=visited, node_highlight=nodes_to_highlight,
                                 edge_highlight=edges_to_highlight)
    return flag_cycles

if __name__ == "__main__":

    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        plot_graph(G)
        # will run only 1 time, assuming Connectivity component = 1
        flag_cycles = has_cycles(G)
        if (flag_cycles):
            print('Plotting of found cycle is available, just uncomment line 32')
            print('The last 2 images are useless, they are created beacuse of the recursion')
            print(f'The graph {filename} has a cycle which is printed above this message')
        else:
            print("Graph doesnt have any cycles")

    print('\n', '-' * 32, '\n')
    print('nx.simple_cycles(G)) - WONT BE USED!')
    print("MAIN PROBLEM - return True doesnt stop the recursion so you cant stop the funtion!")
