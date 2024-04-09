from operator import itemgetter
from queue import PriorityQueue
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph

def dijkstra_sp(G: nx.Graph, higlighted_nodes: list, source_node="0", ) -> dict[Any, list[Any]]:
    unvisited_set = set(G.nodes())
    visited_set = set()
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes
    shortest_paths_len = {} # key = destination node, value = number
    for i in G.nodes:
        shortest_paths_len[i] = np.inf

    #strting node initialisation
    shortest_paths_len[source_node] = 0
    shortest_paths[source_node] = [source_node]
    visited_set.add(source_node)
    unvisited_set.remove(source_node)
    higlighted_nodes.append(source_node)
    # ---

    #while unvisited_set:
    #G[source_node][i]['weight']
    for all_nodes in G.nodes():
        if(all_nodes in unvisited_set):
            for all_edges in nx.neighbors(G, all_nodes):
                print(all_nodes,all_edges)
                # if all_edges[0] in visited_set and all_edges[1] in unvisited_set:
                #     if all_edges['weight'] < shortest_paths_len[ all_edges[1] ] :
                #         print(all_edges, shortest_paths[all_edges[1]])

    return shortest_paths



def dijkstra_sp_with_priority_queue(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    # unvisited_set = set()
    visited_set = set()
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.Graph)
    #plot_graph(G)
    #shortest_paths = dijkstra_sp_with_priority_queue(G, source_node="0")

    test_node = "5"
    nodes_to_higlight = []
    shortest_paths = dijkstra_sp(G, source_node="0",higlighted_nodes=nodes_to_higlight)
    plot_graph(G, highlighted_nodes=nodes_to_higlight)
    # shortest_path_edges = [
    #     (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
    #     for i in range(len(shortest_paths[test_node]) - 1)
    # ]
    #plot_graph(G, highlighted_edges=shortest_path_edges)
