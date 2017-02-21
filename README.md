# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: When 2 numbers are the only possible values in 2 squares of the same unit, we know that such squares will be filled with the 2 values, making those values unavailable to other peers in the unit. We can eliminate the possibility of these 2 values being used for other square (constraint propagation).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: First, we break down the grid into units of rows, columns, block and the 2 diagonal lines. For each determined square A (either pre-filled or one that has only one possible value), we eliminate the possibility of A's value being used for other squares in each of the unit that A belongs to (constraint propagation).

Constraint propagation alone is not sufficient here however. We also need to apply search technique after all constraints has been exploited. At each level of the search, we re-apply the above constraint propagation technique to find more squares' value and thus reduce the depth of the search tree.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
