import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history
NDArrayInt = NDArray[np.int_]


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
    
    random_number_of_changes = np.random.randint(low=0, high=10)
    random_index_start = np.random.randint(low=0, high=len(colors) - random_number_of_changes)
    for i in range(random_number_of_changes):
        new_colors[random_index_start + i] = random_color = np.random.randint(low=0, high=n_max_colors)
        
    return new_colors

def change(iteration_number):
    change = 1 / ( np.log(iteration_number + 195) * 0.1896 )
    return change


def temp_drop(current_temp,min_temp,max_temp,iteration_number) -> float:
    current_temp = current_temp * change(iteration_number)
    if(current_temp <= min_temp):
        current_temp = 0
    return current_temp

def probability(current_temp,delta_conflicts):
    probability_of_transition = 0
    if(current_temp != 0):
        power_of_e = (abs(delta_conflicts)/current_temp) # start = 0 end = inf
        probability_of_transition = np.exp(-1*power_of_e)
    return probability_of_transition

def solve_via_simulated_annealing (G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int):
    current_iteration = 0
    loss_history = np.zeros((n_iters,), dtype=np.float64)
    MIN_TEMP = 0.0000001
    MAX_TEMP = 500
    current_temp = MAX_TEMP
    cur_colors = initial_colors
    
    while(current_iteration < n_iters):
        next_colors = initial_colors.copy()
        next_colors = tweak(next_colors, n_max_colors)
        delta_conflicts = number_of_conflicts(G,cur_colors) - number_of_conflicts(G,next_colors)

        if(delta_conflicts > 0):
            cur_colors = next_colors
        else:
            if(current_temp > MIN_TEMP):
                probability_of_transition = probability(current_temp=current_temp,delta_conflicts=delta_conflicts)
                value = np.random.rand()
                if(value <= probability_of_transition):
                    print(f'JUUUMP!, probability = {probability_of_transition}')
                    cur_colors = next_colors
        
        current_temp = temp_drop(current_temp,MIN_TEMP,MAX_TEMP,current_iteration)
        loss_history[current_iteration] = number_of_conflicts(G,cur_colors)
        current_iteration += 1
        print(f'---\n iteration_number = {current_iteration}, temp = {current_temp}, conflicts={number_of_conflicts(G,cur_colors)}, delta=  {delta_conflicts}\n---')
        
    
    
    return loss_history


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    #plot_graph(G)

    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))


    probabilty_history = np.zeros((n_max_iters,), dtype=np.float64)
    
    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    print(f'FINAL VALUE = {loss_history[-1]}')
    plot_loss_history(loss_history)
