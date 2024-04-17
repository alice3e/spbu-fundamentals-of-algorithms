from typing import Any
from src import plotting
import networkx as nx
from numpy import Inf

def bfs(G: nx.Graph, start_node: Any, end_node: Any):
    dist = {i:Inf for i in G.nodes}
    parent = {i:None for i in G.nodes}
    queue = []
    dist[start_node] = 0
    parent[start_node] = -1
    queue.append(start_node)
    while(queue):
        current_node = queue.pop(0)
        for neighbours in G.neighbors(current_node):
            if dist[neighbours] > dist[current_node] + 1:
                dist[neighbours] = dist[current_node] + 1;
                parent[neighbours] = current_node;
                queue.append(neighbours)
    min_flow = Inf
    path = []
    current_node = end_node
    for i in range(dist[end_node]):
        path.append(current_node)
        min_flow = min(min_flow, G.get_edge_data(parent[current_node],current_node)['weight'])
        current_node = parent[current_node]
    path.append(start_node)
    path = path[::-1]
    return zip(min_flow,path)

# Алгоритм Эдмондса — Карпа
def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    #print(neighbours, G.get_edge_data(current_node,neighbours)['weight'])
    # weight - макс пропуск способ
    # ДЗ найти еще более сложные графы и поиграть с ними
    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    
    print(bfs(G,'0','5'))
    
    
    plotting.plot_graph(G)
    #val = max_flow(G, s=0, t=5)
    #print(f"Maximum flow is {val}. Should be 23")
#typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet