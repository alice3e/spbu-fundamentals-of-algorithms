from operator import itemgetter
from queue import PriorityQueue
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def dijkstra_sp_with_priority_queue(
    G: nx.Graph, source_node="0"
) -> dict[Any, list[Any]]:
    # unvisited_set = set()
    visited_set = set()
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp_with_priority_queue(G, source_node="0")
    test_node = "5"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
