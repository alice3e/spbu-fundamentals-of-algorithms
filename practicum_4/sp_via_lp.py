from copy import copy

import numpy as np
import networkx as nx
from scipy.optimize import linprog

from src.plotting import plot_graph


def build_edge_idx_to_adj_matrix_idx_map(adj_matrix):
    edge_idx_to_adj_matrix_idx_map = {}
    edge_idx = 0
    for i in range(adj_matrix.shape[0]):
        for j in range(adj_matrix.shape[1]):
            if adj_matrix[i, j] != 0:
                edge_idx_to_adj_matrix_idx_map[edge_idx] = (i, j)
                edge_idx += 1
    return edge_idx_to_adj_matrix_idx_map


def solve_via_lp(G, s_node, t_node):
    nodes = list(G.nodes)
    n_nodes = len(nodes)
    s_i = nodes.index(s_node)
    t_i = nodes.index(t_node)
    adj_matrix = nx.adjacency_matrix(G).todense()

    edge_mask = adj_matrix != 0
    c = adj_matrix[edge_mask].reshape(-1)

    A_eq = np.zeros((n_nodes, len(c)), dtype=np.int_)
    node_indices = list(range(n_nodes))
    for i in range(n_nodes):
        rowcol_selector = copy(node_indices)
        rowcol_selector.remove(i)
        temp = adj_matrix.copy()
        temp[i, :][temp[i, :] != 0] = -1
        temp[:, i][temp[:, i] != 0] = 1
        temp[np.ix_(rowcol_selector, rowcol_selector)] = 0
        A_eq[i] = temp[edge_mask]

    rowcol_selector = copy(node_indices)
    rowcol_selector.remove(s_i)
    A_eq = A_eq[rowcol_selector]

    b_eq = np.zeros((n_nodes,), dtype=np.int_)
    b_eq[t_i] = 1
    b_eq = b_eq[rowcol_selector]

    res = linprog(c, A_ub=None, b_ub=None, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))

    edge_idx_to_adj_matrix_idx_map = build_edge_idx_to_adj_matrix_idx_map(adj_matrix)
    shortest_path_edges = []
    for i, path_segment_value in enumerate(res.x):
        if path_segment_value != 0.0:
            in_idx, out_idx = edge_idx_to_adj_matrix_idx_map[i]
            edge = nodes[in_idx], nodes[out_idx]
            shortest_path_edges.append(edge)
    return shortest_path_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"
    shortest_path_edges = solve_via_lp(G, s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
