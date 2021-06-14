import cv2 as cv2
import numpy as np

from cellularAutomataV1 import LangtonAnts

#%%

width = 400
height = 200

n_ants = 5

n_step = 100
# n_step = 0

ca_grid = LangtonAnts(width, height, n_ants = n_ants)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)

ca_grid.computeNStep(n_step)


while(True):
    cv2.imshow("Cells", ca_grid.draw_cells)
    
    ca_grid.update()
    
    if cv2.waitKey(1) == ord('q'):
        break
    