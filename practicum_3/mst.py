from typing import Any

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST

    mst_set.add(start_node)
    rest_set.remove(start_node)
    while rest_set:
        edge_to_add = {
            "edge": (None , None),
            "weight": np.inf,
        }
        node_to_add = None
        for node in mst_set: # optimise!
            for neight_node in G.neighbors(node):
                if(neight_node in mst_set):
                    continue
                else:
                    if G[node][neight_node]["weight"] < edge_to_add["weight"]:
                        edge_to_add["edge"] = (node, neight_node)
                        edge_to_add["weight"] = G[node][neight_node]["weight"]
                        node_to_add = neight_node
        mst_edges.add(edge_to_add["edge"])
        mst_set.add(node_to_add)
        rest_set.remove(node_to_add)

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
    print()