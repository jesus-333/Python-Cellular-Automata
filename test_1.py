import cv2 as cv2
import numpy as np

from cellularAutomataV1 import cellularAutomataV1

#%%

width = 400
height = 200


ca_grid = cellularAutomataV1(width, height)
ca_grid.randomSeed(0.7)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 1000, 500)


while(True):
    cv2.imshow("Cells", ca_grid.cells)
    
    ca_grid.update()
    
    # cv2.waitKey(0)
    
    if cv2.waitKey(1) == ord('q'):
        break
    