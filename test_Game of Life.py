import cv2 as cv2
import numpy as np

from library.game_of_life import GameOfLife

#%%

width = 200
height = 100

step = 0


ca_grid = GameOfLife(width, height)
ca_grid.randomSeed(0.55)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)


while(True):
    cv2.imshow("Cells", ca_grid.cells)
    
    ca_grid.update()
    
    # cv2.waitKey(0)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    step += 1
    
    # if(step == 25):
    #     step = 0
    #     ca_grid.setChMatrixRandom()
    
