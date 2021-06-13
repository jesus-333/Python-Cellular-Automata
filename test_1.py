import cv2 as cv2
import numpy as np

from cellularAutomataV1 import cellularAutomataV1

#%%

width = 400
height = 200


ca_grid = cellularAutomataV1(width, height)
ca_grid.randomSeed(0.2)


while(True):
    ca_grid.update()
    
    cv2.imshow("Cells", ca_grid.cells)
    
    if cv2.waitKey(1) == ord('q'):
        break
    