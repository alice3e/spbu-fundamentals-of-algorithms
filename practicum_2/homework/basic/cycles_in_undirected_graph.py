import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph):
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist("practicum_2/homework/graph_2.edgelist", create_using=nx.Graph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
