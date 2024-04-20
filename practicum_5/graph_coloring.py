from mimetypes import init
from typing import Protocol

import numpy as np
import networkx as nx

from src.common import NDArrayInt
from src.plotting import plot_graph, plot_loss_history


class GraphColoringSolver(Protocol):
    def __call__(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
    ) -> NDArrayInt:
        pass


def number_of_conflicts(G, colors):
    set_colors(G, colors)
    n = 0
    for n_in, n_out in G.edges:
        if G.nodes[n_in]["color"] == G.nodes[n_out]["color"]:
            n += 1
    return n


def set_colors(G, colors):
    for n, color in zip(G.nodes, colors):
        G.nodes[n]["color"] = color


def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    n_nodes = len(new_colors)
    random_i = np.random.randint(low=0, high=n_nodes)
    random_color = np.random.randint(low=0, high=n_max_colors)
    new_colors[random_i] = random_color
    return new_colors


def solve_via_hill_climbing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    n_tweaks = 10
    cur_colors = initial_colors
    next_colors = initial_colors.copy()
    next_colors_best = initial_colors.copy()
    for i in range(n_iters):
        loss_history[i] = number_of_conflicts(G, cur_colors)
        next_colors_best = tweak(cur_colors, n_max_colors)
        n_conflicts_best = number_of_conflicts(G, next_colors_best)
        for _ in range(n_tweaks):
            next_colors = tweak(cur_colors, n_max_colors)
            if number_of_conflicts(G, next_colors) < n_conflicts_best:
                next_colors_best = next_colors
                n_conflicts_best = number_of_conflicts(G, next_colors)
        if n_conflicts_best < number_of_conflicts(G, cur_colors):
            cur_colors = next_colors_best
    return loss_history


def solve_via_random_search(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    for i in range(n_iters):
        colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))
        loss_history[i] = number_of_conflicts(G, colors)
    return loss_history


def solve_with_restarts(
    solver: GraphColoringSolver,
    G: nx.Graph,
    n_max_colors: int,
    initial_colors: NDArrayInt,
    n_iters: int,
    n_restarts: int,
) -> NDArrayInt:
    loss_history = np.zeros((n_restarts, n_iters), dtype=np.int_)
    for i in range(n_restarts):
        print(f"Restart #{i + 1}")
        initial_colors = np.random.randint(
            low=0, high=n_max_colors - 1, size=len(G.nodes)
        )
        set_colors(G, initial_colors)
        loss_history_per_run = solver(G, n_max_colors, initial_colors, n_max_iters)
        loss_history[i, :] = loss_history_per_run
    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    # loss_history = solve_via_random_search(G, n_max_colors, initial_colors, n_max_iters)
    # plot_loss_history(loss_history)

    # loss_history = solve_via_hill_climbing(G, n_max_colors, initial_colors, n_max_iters)
    # plot_loss_history(loss_history)

    n_restarts = 10
    loss_history = solve_with_restarts(
        solve_via_hill_climbing,
        G,
        n_max_colors,
        initial_colors,
        n_max_iters,
        n_restarts,
    )
    plot_loss_history(loss_history)