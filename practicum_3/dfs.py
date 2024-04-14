import queue
from typing import Any
import networkx as nx
from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_iterative(G: nx.Graph, node_name: Any, visited: dict[Any]) -> None:
    node_highlight = []
    current = []
    current.append(node_name)
    while (current):
        current_vertex = current.pop()
        node_highlight.append(current_vertex)
        visited[current_vertex] = True
        for neighbor in nx.all_neighbors(G, current_vertex):
            if (visited[neighbor] == False and (neighbor not in current)):
                current.append(neighbor)
        plot_graph(G, highlighted_nodes=node_highlight)


# Разница между двумя алгоритмами заключается в порядке посещения узлов.
#
# В функции dfs_recursive_postorder мы сначала рекурсивно обходим всех соседей узла, а затем выводим сам узел.
# Такой порядок называется "пост-порядком" (postorder) и означает, что мы сначала обходим всех потомков узла, а затем выводим сам узел.
#
# В то время как в функции dfs_recursive мы сначала выводим узел, а затем рекурсивно обходим всех его соседей.
# Этот порядок называется "пред-порядком" (preorder) и означает, что мы сначала выводим узел, а затем обходим всех его потомков.
# НО! так как наш алгоритм ничего не печатает и не возвращает, то разница нет
# P.S. Добавил в plot_graph() функцию покраски вершин графа поэтому попоытался отразить разницу через рисование графов пошагово



node_highlight = []
def dfs_recursive(G: nx.Graph, node_name: Any, visited: dict[Any]) -> None:
    global node_highlight
    visited[node_name] = True
    node_highlight.append(node_name)  # вся разница в расположении этой строчки
    visit(node_name)
    for neighbor in G.neighbors(node_name):
        if not visited[neighbor]:
            node_highlight.append(neighbor)
            plot_graph(G, highlighted_nodes=node_highlight)
            dfs_recursive(G, neighbor, visited)


def dfs_recursive_postorder(G: nx.DiGraph, node_name: Any, visited: dict[Any]) -> None:
    global node_highlight
    visited[node_name] = True

    for neighbor in G.neighbors(node_name):
        if not visited[neighbor]:
            node_highlight.append(neighbor)
            plot_graph(G, highlighted_nodes=node_highlight)
            dfs_recursive_postorder(G, neighbor, visited)
    visit(node_name)
    node_highlight.append(node_name)  # вся разница в расположении этой строчки


if __name__ == "__main__":
    # Load and plot the graph
    # G = nx.erdos_renyi_graph(n=15, p=0.2)  # кол-во узлов, вероятность появления связи
    G = nx.read_edgelist("practicum_3/graph_2.edgelist", create_using=nx.Graph)
    plot_graph(G)

    # 1. Recursive DFS. Trivial to implement, but it does not scale on large graphs
    # In the debug mode, look at the call stack
    print("Recursive DFS")
    print("-" * 32)
    visited = {n: False for n in G}
    dfs_recursive(G, node_name=list(nx.nodes(G))[0], visited=visited)

    # 2. Iterative DFS. Makes use of LIFO/stack data structure, does scale on large graphs
    # print("Iterative DFS")
    # print("-" * 32)
    # dfs_iterative(G, node="0")
    # print()

    # 3. Postorder recursive DFS for topological sort
    # If a directed graph represent tasks to be done, the topological sort tells
    # us what the task order should be, i.e. scheduling
    # Postorder DFS outputs the reversed order!
    # G = nx.read_edgelist("graph_2.edgelist", create_using=nx.DiGraph)
    # plot_graph(G)
    # print("Postorder iterative DFS")
    # print("-" * 32)
    # visited = {n: False for n in G}
    # dfs_recursive_postorder(G, node="0", visited=visited)

# %%
