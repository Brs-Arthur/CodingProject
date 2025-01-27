"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import tkinter as tk 
class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self): 
        """
        Plots a visual representation of the grid.
        """
        x_size = 1000/self.m
        y_size = 1000/self.n
        root = tk.Tk()
        can = tk.Canvas(root)
        for i in range(self.n):
            for j in range(self.m):
                can.create_rectangle(i*x_size,j*x_size,(i+1)*x_size,(j+1)*x_size,outline='black')
                can.pack(expand=1)
        root.mainloop()

    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return self.colors_list[self.color[i][j]] == "k"

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        return abs(self.value[pair[0][0]][pair[0][1]]-self.value[pair[1][0]][pair[1][1]])


    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """
        pairs = []
        L = [(i,j) for i in range(self.n) for j in range(self.m)]
        # Remove the element of L at i,j
        #Creation pairs loop
        for (i,j) in L:
            #Not a black case
            if not self.is_forbidden(i,j): 
                # Pattern condition: (the case exists) and (the case hasn't been already tested) and (the color is the same)
                # Top Element
                if (i > 0) and ((i-1, j) in L) and (self.color[i-1][j] == self.color[i][j]):
                    pairs.append(((i,j),(i-1,j)))
                #Bottom Element
                if (i < self.n) and ((i+1, j) in L) and (self.color[i+1][j] == self.color[i][j]):
                    pairs.append(((i,j),(i+1,j)))
                #Right Element 
                if (j > 0) and ((i, j-1) in L) and (self.color[i][j-1] == self.color[i][j]):
                    pairs.append(((i,j),(i,j-1)))
                #Left Element 
                if (j < self.m) and ((i, j+1) in L) and (self.color[i][j+1] == self.color[i][j]):
                    pairs.append(((i,j),(i,j+1)))
            #Remove the first element already tested
            L = L[1:]
        return pairs

    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid


