from grid import Grid
from solver import *

grid = Grid(2, 3)

data_path = "./input/"

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name)

file_name = data_path + "grid00.in"
grid = Grid.grid_from_file(file_name, read_values=True)
grid.plot()


solver = SolverEmpty(grid)
solver.run()
print("The final score of SolverEmpty is:", solver.score())


