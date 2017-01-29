# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins are Sudoku boxes having identical values along one of the following-- row, columns or grid squares. 

Identical value across two boxes in the same unit enforces the constraint that no other box in the same unit can contain the same value. This in turn helps in reducing the  search space. As the localization constraint is enforced it further introduces new constraints for other parts of the board that can help us further reduce the number of possibilities -- The well known divide and conquer strategy

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Digonal Suduko has an additional requirement -- all the boxes along the diagonals MUST have the digit appearing only once. This requires us to account for additional boxes along the diagonals and applly the techniques of Eimination, Only choice, Search and Naked Twins along the diagonal boxes. 

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
