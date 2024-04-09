from typing import Any

import networkx as nx


def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    # weight - макс пропуск способ
    # ДЗ найти еще более сложные графы и поиграть с ними
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    
    val = max_flow(G, s=0, t=5)
    print(f"Maximum flow is {val}. Should be 23")
