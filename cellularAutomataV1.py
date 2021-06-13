"""
Created on Sun Jun 13 21:49:12 2021

@author: jesus
"""

#%%

import numpy as np

#%%

class cellularAutomataV1():
    
    def __init__(self, width, height, cells_to_live = 3, cells_die_alone = 2, cells_overpopulation = 4):
        self.width = width
        self.height = height
        
        self.cells = np.zeros((height, width))
        self.ghost_cells = np.zeros((height, width))
        
        self.cells_to_live = 3
        self.cells_die_alone = 2
        self.cells_overpopulation = 4
        
        
    def randomSeed(self, p = 0.5):
        #Initialize at random some elements
        
        # Create random matrix
        tmp_random = np.random.rand(self.height, self.width)
        
        # Set the cells alive according to random inizialization
        self.cells[tmp_random > p] = 1
        self.ghost_cells[tmp_random > p] = 1
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Update functions
        
    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                tmp_value = self.updateCell(i, j)
                
                if(tmp_value == 0): self.ghost_cells[i, j] = 0
                else: self.ghost_cells[i, j] += 1
                
        np.copyto(self.cells, self.ghost_cells)
                
    
    def updateCell(self, i, j):
        n_cells_neighbor = 0
        return_value = -1
        
        
        n_cells_neighbor += self.checkUp(i, j)
        n_cells_neighbor += self.checkRight(i, j)
        n_cells_neighbor += self.checkDown(i, j)
        n_cells_neighbor += self.checkLeft(i, j)
        
        if(self.cells[i, j] == 0): # If the cell is dead
            if(n_cells_neighbor == self.cells_to_live): return_value = 1
            else: return_value = 0
            
            return return_value;
        elif(self.cells[i, j] > 0): # If the cell is alive
            
            # Cell die for loneliness
            if(n_cells_neighbor < self.cells_die_alone): return_value = 0
            
            # Cell survive
            if(n_cells_neighbor > self.cells_die_alone and n_cells_neighbor < self.cells_overpopulation): return_value = 1
            
            # Cell die for overpopulation
            if(n_cells_neighbor >= self.cells_overpopulation): return_value = 0
            
            return return_value
            
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Check functions (CROSS)
    
    def checkUp(self, i, j):
        if(i == 0): 
            tmp_cell = self.cells[self.height - 1, j]
        else: 
            tmp_cell = self.cells[i - 1, j]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkDown(self, i, j):
        if(i == (self.height - 1)): 
            tmp_cell = self.cells[0, j]
        else: 
            tmp_cell = self.cells[i + 1, j]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkLeft(self, i, j):
        if(j == 0): 
            tmp_cell = self.cells[i, self.width - 1]
        else: 
            tmp_cell = self.cells[i, j - 1]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkRight(self, i, j):
        if(j == (self.width - 1)): 
            tmp_cell = self.cells[i, 0]
        else: 
            tmp_cell = self.cells[i, j + 1]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Check functions (DIAGONAL)
    
    def checkUp(self, i, j):
        if(i == 0): 
            tmp_cell = self.cells[self.height - 1, j]
        else: 
            tmp_cell = self.cells[i - 1, j]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkDown(self, i, j):
        if(i == (self.height - 1)): 
            tmp_cell = self.cells[0, j]
        else: 
            tmp_cell = self.cells[i + 1, j]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkLeft(self, i, j):
        if(j == 0): 
            tmp_cell = self.cells[i, self.width - 1]
        else: 
            tmp_cell = self.cells[i, j - 1]
        
        if(tmp_cell > 0): return 1
        else: return 0
        
    def checkRight(self, i, j):
        if(j == (self.width - 1)): 
            tmp_cell = self.cells[i, 0]
        else: 
            tmp_cell = self.cells[i, j + 1]
        
        if(tmp_cell > 0): return 1
        else: return 0
