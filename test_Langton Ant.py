import cv2 as cv2
import numpy as np

from cellularAutomataV1 import LangtonAnts

#%%

width = 200
height = 100

n_ants = 6

ca_grid = LangtonAnts(width, height, n_ants = n_ants)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)


while(True):
    cv2.imshow("Cells", ca_grid.draw_cells)
    
    ca_grid.update()
    
    if cv2.waitKey(1) == ord('q'):
        break
    