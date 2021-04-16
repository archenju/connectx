import numpy as np


class Board():
    def __init__(self, columns: int):
        self.keepplaying = True
        self.rows = 6
        self.cols = columns
        self.maxturns = self.rows * self.cols
        self.grid = np.zeros(shape=(self.rows, self.cols), dtype=int)
        self.winner = 0
        #print(self.grid)
        #print("Board created")
    
    def insert(self, col: int, player: int, trial=False) -> int:
        if col < 0 or col > self.cols:
            return -1
        targetcol = self.grid[:, col]
        if 0 not in targetcol:
            return -1 # This column is already full
        else:
            for i in range(self.rows):
                if targetcol[i] == 0:
                    if not trial:
                        targetcol[i] = player
                        self.maxturns = self.maxturns - 1
                    return i
    
    def reset(self):
        self.grid = np.zeros(shape=(self.rows, self.cols), dtype=int)
        self.keepplaying = True
        self.maxturns = self.rows * self.cols
                   
    def display(self) -> None:
        for i in range(self.rows-1, -1, -1): # Invert the display so that row 1 is at the bottom
            line = "|"
            for j in range(self.cols):
                item = int( self.grid[i, j] )
                if item == 1:
                    item = "X"
                elif item == -1:
                    item = "O"
                else:
                    item = " "
                line = line + item  + "|"
            print(line)
        print( " _"*self.cols )
        print("")



