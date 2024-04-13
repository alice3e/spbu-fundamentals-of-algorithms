import networkx as nx

from src.plotting import plot_graph


def solve_via_lp(G, s_node, t_node):
    shortest_path_edges = []

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    return shortest_path_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)

    s_node = "0"
    t_node = "5"
    shortest_path_edges = solve_via_lp(G, s_node=s_node, t_node=t_node)
    plot_graph(G, highlighted_edges=shortest_path_edges)
