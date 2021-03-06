#%% Imports

import numpy as np

#%%


class GameOfLife():
    
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
        
        self.setChMatrixRandom()
        
    def setChMatrixRandom(self): self.ch_matrix = np.random.randint(0, 3, (self.height, self.width))
        
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
        

#%% Langton's ant

class LangtonAnts():
    
    def __init__(self, width, height, n_ants = 1, reproduction = False):
        # Dimensions of the grid
        self.width = width
        self.height = height
        
        # Grid variables
        self.cells = np.zeros((height, width))
        self.ghost_cells = np.zeros((height, width))
        self.draw_cells = np.zeros((height, width, 3))
        
        # List of the ants
        self.list_of_ants = []
        
        # Values for the direction
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        
        # Random inizialization
        for i in range(n_ants):
            self.list_of_ants.append(self.createAnt(i))
        
        # Reproduction value
        self.reproduction = reproduction
        self.reproduction_max_distance = 10
            
    def createAnt(self, i, x = -1, y = -1):
        # Assign position (if passed) or set a random position in the grid
        if(x != -1 and y != -1): tmp_position = [y, x]
        else: tmp_position = [np.random.randint(0, self.height, 1)[0], np.random.randint(0, self.width, 1)[0]]
        
        # Assign random color
        tmp_color = (np.random.random(1)[0], np.random.random(1)[0], np.random.random(1)[0])
        
        # Assign random direction
        tmp_direction = np.random.randint(0, 4, 1)[0]
        
        # Create ant
        tmp_ant = {'id':i, 'position':tmp_position, 'color':tmp_color, 'direction':tmp_direction}
        
        return tmp_ant
    
    def setColor(self, list_of_colors):
        if(len(self.list_of_ants) != len(list_of_colors)): raise ValueError('Length of list of ants and list of colors are different.')
        
        for ant, color in zip(self.list_of_ants, self.list_of_colors):
            ant['color'] = color
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Update functions
        
    def update(self):
        for ant in self.list_of_ants: 
            # Rotate the ant and change the color
            ant['direction'] = self.rotateAnt(ant)
            
            # Move the ant
            ant['position'] = self.moveAnt(ant)
            
            if(self.reproduction and len(self.list_of_ants) < 400): self.reproduceAnts()
        
        # Update all the states together
        np.copyto(self.cells, self.ghost_cells)
        
        
    def computeNStep(self, n): 
        for i in range(n): self.update()
            
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Rotate functions
            
    def rotateAnt(self, ant):
        # Retrieve ant position and the state of the corresponding cell
        i, j = ant['position']       
        cell_state = self.cells[i, j]
        
        if(cell_state == 0): # Black cell
            self.ghost_cells[i, j] = 1
            self.draw_cells[i, j] = np.asarray(ant['color'])
            return self.rotateClockwise(ant['direction'])
        else: # Colored cell
            self.ghost_cells[i, j] = 0
            self.draw_cells[i, j] = np.asarray([0, 0, 0])
            return self.rotateAnticlockwise(ant['direction'])
        
    
    def rotateClockwise(self, direction): return self.UP if direction >= self.LEFT else direction + 1
    def rotateAnticlockwise(self, direction): return self.LEFT if direction <= self.UP else direction - 1
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Movement functions
    
    def moveAnt(self, ant):
        i, j = ant['position']
        direction = ant['direction']
        
        if(direction == self.UP):   return [self.moveUp(i),     j]
        if(direction == self.RIGHT): return [i,                  self.moveRight(j)]
        if(direction == self.DOWN): return [self.moveDown(i),   j]
        if(direction == self.LEFT): return [i,                  self.moveLeft(j)]
            
        
    def moveUp(self, i):    return self.height - 1 if i == 0 else i - 1
    def moveDown(self, i):  return 0 if i == self.height - 1 else i + 1
    def moveRight(self, j): return self.width - 1 if j == 0 else j - 1
    def moveLeft(self, j):  return 0 if j == self.width - 1 else j + 1
    
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Reproduction function
    # TODO correct bug
    
    def reproduceAnts(self):
        list_new_ants = []
        
        # Cycle thorugh the ants
        for ant in self.list_of_ants:
            for other_ant in self.list_of_ants:
                
                # Check to not select the same ant
                if(ant['id'] != other_ant['id']):
                    
                    # Evaluate distane between two ants
                    y1, x1 = ant['position']
                    y2, x2 = other_ant['position']
                    tmp_distance = np.sqrt((x1 - x2)**2 + (y1 - y1)**2)
                    
                    # If they are close enough a new ant born
                    if(tmp_distance < self.reproduction_max_distance):
                        # tmp_ant = self.createAnt(len(self.list_of_ants) + len(list_new_ants), int((x1 + x2)/2), int((y1 + y2)/2))
                        tmp_ant = self.createAnt(len(self.list_of_ants) + len(list_new_ants))
                        list_new_ants.append(tmp_ant)
         
        # Add the new ant to list
        for new_ant in list_new_ants: self.list_of_ants.append(new_ant)
    