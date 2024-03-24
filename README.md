# spbu-fundamentals-of-algorithms
Materials for the practicum for "Fundamentals of Algorithms" course at SpbU

## Getting started

Set up your environment

### VSCode

Go to `Run and Debug` in the left panel, create a new launch file, select `Python File` and add the following field:
```yaml
"env": {
    "PYTHONPATH": "${workspaceFolder}${pathSeparator}${env:PYTHONPATH}"
}
```

### MacOs (homebrew or python.app)
Go to `Terminal.app` and paste this command:
```bash
export PYTHONPATH=/Users/path_to_your_github_clone_directory:$PYTHONPATH
```
### MacOs (anaconda3 or miniconda)
Go to `Terminal.app` and paste this command:
```bash
conda develop /Users/path_to_your_github_clone_directory
```
Then you can check you PYTHONPATH with this command
```bash
python -c "import sys; print('\n'.join(sys.path))"
```
*Note: python inside your console and inside your PyCharm/Jupyter/DataSpell may be different so run commands in terminal of this app*

Another way to check your PYTHONPATH (most accurate)
paste this code (first line) in some .py file (for example: practicum_2/dfs.py ) and run the file
```python
print(sys.path) # you should see /Users/path_to_your_github_clone_directory
```

## Practicum 1

We study basic tools necessary for the rest of the course: `python`, `numpy` and  `matplotlib`. It is assumed that a student has some decent knowledge of python though he/she is not very experienced in it.

Plan:
1. Warm-up
2. Go through `intro_to_numpy_and_matplotlib.ipynb` together

## Practicum 2

We start working on graph algorithms via introducing `networkx` and then a couple of simple algorithm for graph traversals.

Plan:
1. Warm-up
2. Go through `intro_to_networkx.ipynb` together
3. Complete `bfs_maze_template.py`
4. Go through `dfs_recursive()` in `dfs_maze.py` together
5. Complete `dfs_iterative()` in `dfs_maze_template.py`
6. Complete `topological_sort()` in `dfs_maze_template.py`
7. Go through `dfs_recursive_postorder()` in `dfs_maze.py` together (solution for point 6)

## Practicum 3

We study two classical graph problems: Minimum Spanning Tree and Shortest Path. We use Prim's algorithm to solve the former and Dijkstra's algorithm to solve the latter.

Plan:
1. Warm-up
2. Complete `mst_template.py`
3. Complete `sp_template.py`. We can do both the original version and the version with a priority queue.

## Practicum 4

We study fundamental data structures.

Plan:
1. Warm-up
2. Complete `valid_parentheses.py` (LIFO)
3. Complete `time_needed_to_buy_tickets.py` (FIFO)
4. Complete `linked_list.py` (linked list)

Homework:
1. `time_needed_to_buy_tickets.py`: implement a proper solution for this problem.

## Practicum 5

We study simple computaional geomtery algorithms such as convex hull computing.

Plan:
1. Warm-up
2. Complete `slow_convex_hull.py`
3. Complete `qwer`

Homework:
1. `convex_bucket.py`: implement a convex hull algorithm constructing only the lower part of a convex hull which would "hold" all the points if they fell due to the gravity.

## Practicum 10

Cubic spline: http://getsomemath.ru/subtopic/computational_mathematics/approximation_theory/local_interpolation

LU: http://getsomemath.ru/subtopic/computational_mathematics/numerical_linear_algebra/gauss_methods
