from typing import Any
from src import plotting
import networkx as nx
from numpy import Inf


# В остаточной сети находим кратчайший путь из источника в сток.
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
    if(dist[end_node] == Inf): return ([-1],[-1])
    for i in range(dist[end_node]):
        path.append(current_node)
        min_flow = min(min_flow, G.get_edge_data(parent[current_node],current_node)['weight'])
        current_node = parent[current_node]
    path.append(start_node)
    path = path[::-1]
    return ([min_flow],path)

# Пускаем через найденный путь (он называется увеличивающим путём или увеличивающей цепью) максимально возможный поток: 
def weight_change(G: nx.Graph, start_node: Any , end_node:Any, path: list, min_flow: int) -> None:
    edge_higlight = []
    print(path,min_flow)
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i+1]
        G[start][end]['weight'] -= min_flow
        if(G[start][end]['weight'] == 0): G.remove_edge((start),(end))
        G.add_edge(end,start,weight=min_flow)
        edge_higlight.append((start,end))
    plotting.plot_graph(G,highlighted_edges=edge_higlight)

# Алгоритм Эдмондса — Карпа
def max_flow(G: nx.Graph, s: Any, e: Any) -> int:
    value: int = 0
    cur_flow, path = bfs(G,s,e)
    cur_flow = cur_flow[0]
    while(cur_flow >= 0): #В остаточной сети находим кратчайший путь из источника в сток. Если такого пути нет, останавливаемся.
        value += cur_flow
        print(f'cur_flow = {cur_flow} , path - {path}, value = {value}')
        weight_change(G,s,e,path,cur_flow)
        cur_flow, path = bfs(G,s,e)
        cur_flow = cur_flow[0]
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_2.edgelist", create_using=nx.DiGraph)
    val = max_flow(G, s='0', e='5')
    print(f"Maximum flow is {val}. Should be 23")
