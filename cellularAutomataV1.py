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
        
        self.cells = np.zeros((height, width, 3))
        self.ghost_cells = np.zeros((height, width, 3))
        
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
        
        self.ch_matrix = np.random.randint(0, 3, (self.height, self.width))
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Update functions
        
    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                tmp_value = self.updateCell(i, j)
                
                if(tmp_value == 0): self.ghost_cells[i, j] = 0
                else: 
                    self.ghost_cells[i, j, self.ch_matrix[i, j]] += 1
                    if(self.ghost_cells[i, j, self.ch_matrix[i, j]] > 255): self.ghost_cells[i, j, self.ch_matrix[i, j]] = 1
                     
        np.copyto(self.cells, self.ghost_cells)
                
    
    def updateCell(self, i, j):
        n_cells_neighbor = 0
        return_value = -1
        
        n_cells_neighbor += self.checkUp(i, j)
        n_cells_neighbor += self.checkUpRight(i, j)
        n_cells_neighbor += self.checkRight(i, j)
        n_cells_neighbor += self.checkDownRight(i, j)
        n_cells_neighbor += self.checkDown(i, j)
        n_cells_neighbor += self.checkDownLeft(i, j)
        n_cells_neighbor += self.checkLeft(i, j)
        n_cells_neighbor += self.checkUpLeft(i, j)
        
        if(self.cells[i, j, self.ch_matrix[i, j]] == 0): # If the cell is dead
            if(n_cells_neighbor == self.cells_to_live): return_value = 1
            else: return_value = 0
            
            return return_value;
        elif(self.cells[i, j, self.ch_matrix[i, j]] > 0): # If the cell is alive
            
            # Cell die for loneliness
            if(n_cells_neighbor < self.cells_die_alone): return_value = 0
            
            # Cell survive
            if(n_cells_neighbor > self.cells_die_alone and n_cells_neighbor < self.cells_overpopulation): return_value = 1
            
            # Cell die for overpopulation
            if(n_cells_neighbor >= self.cells_overpopulation): return_value = 0
            
            return return_value
            
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Check functions (CROSS)
    
    def checkUp(self, i, j):    return 1 if(self.cells[self.moveUp(i),      j,                  self.ch_matrix[self.moveUp(i), j]] > 0)     else 0  
    def checkDown(self, i, j):  return 1 if(self.cells[self.moveDown(i),    j,                  self.ch_matrix[self.moveDown(i), j]] > 0)   else 0
    def checkLeft(self, i, j):  return 1 if(self.cells[i,                   self.moveLeft(j),   self.ch_matrix[i, self.moveLeft(j)]] > 0)   else 0
    def checkRight(self, i, j): return 1 if(self.cells[i,                   self.moveRight(j),  self.ch_matrix[i, self.moveRight(j)]] > 0)  else 0
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Check functions (DIAGONAL)
    
    def checkUpLeft(self, i, j):    return 1 if(self.cells[self.moveUp(i),   self.moveLeft(j),  self.ch_matrix[self.moveUp(i),   self.moveLeft(j)]] > 0)  else 0   
    def checkUpRight(self, i, j):   return 1 if(self.cells[self.moveDown(i), self.moveRight(j), self.ch_matrix[self.moveDown(i), self.moveRight(j)]] > 0) else 0  
    def checkDownLeft(self, i, j):  return 1 if(self.cells[self.moveDown(i), self.moveLeft(j),  self.ch_matrix[self.moveDown(i), self.moveLeft(j)]] > 0)  else 0 
    def checkDownRight(self, i, j): return 1 if(self.cells[self.moveDown(i), self.moveRight(j), self.ch_matrix[self.moveDown(i), self.moveRight(j)]] > 0) else 0
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Move functions
    
    def moveUp(self, i):    return self.height - 1 if i == 0 else i - 1
    def moveDown(self, i):  return 0 if i == self.height - 1 else i + 1
    def moveRight(self, j): return self.width - 1 if j == 0 else j - 1
    def moveLeft(self, j):  return 0 if j == self.width - 1 else j + 1
        
