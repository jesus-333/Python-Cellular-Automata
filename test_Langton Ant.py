import cv2 as cv2
import numpy as np

from LangtonAnts import LangtonAnts

#%%

width = 800
height = 400

n_ants = 5

n_step = 300000
# n_step = 0

reproduction = False

ca_grid = LangtonAnts(width, height, n_ants = n_ants, reproduction = reproduction)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)

ca_grid.computeNStep(n_step)


while(True):
    cv2.imshow("Cells", ca_grid.draw_cells)
    
    ca_grid.update()
    
    if cv2.waitKey(1) == ord('q'):
        break
    