import cv2 as cv2
import numpy as np

from LangtonAnts import LangtonAnts
from AutomataMusic import AntsMusic

#%%

width = 108
height = 108

n_ants = 2

# n_step = 300000
n_step = 0

reproduction = False

fs = 44100
sound_duration = 0.5

ca_grid = LangtonAnts(width, height, n_ants = n_ants, reproduction = reproduction)
ca_sound = AntsMusic(width, height, fs = fs, sound_duration = sound_duration)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)

ca_grid.computeNStep(n_step)
sound_map = ca_sound.sound_map

while(True):
    cv2.imshow("Cells", ca_grid.draw_cells)
    
    ca_grid.update()
    
    ca_sound.sound(ca_grid.list_of_ants)
    
    if cv2.waitKey(1) == ord('q'):
        break
    