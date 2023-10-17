import cv2 as cv2
import numpy as np

from library.langton_ant import LangtonAnts
# from AutomataMusic import AntsMusicV1, AntsMusicV2

#%%

width = 1600
height = 900

n_ants = 33

n_step = 1000
# n_step = 0

reproduction = False

fs = 44100
sound_duration = 0.5

ca_grid = LangtonAnts(width, height, n_ants = n_ants, reproduction = reproduction)
ca_grid.computeNStep(n_step)

cv2.namedWindow("Cells", cv2.WINDOW_NORMAL)
cv2.resizeWindow('Cells', 800, 400)

# ca_sound = AntsMusicV2(width, height, fs = fs, sound_duration = sound_duration)
# sound_map = ca_sound.sound_map

colors_1 = [(np.random.random(1)[0], np.random.random(1)[0], np.random.random(1)[0])]
colors_2 = [(np.random.random(1)[0], np.random.random(1)[0], np.random.random(1)[0])]

while(True):
    cv2.imshow("Cells", ca_grid.draw_cells)
    
    ca_grid.update()
    
    # sine_wave = ca_sound.sound(ca_grid.list_of_ants)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
    
#%%

# def rescale(x, a = 0, b = 1):
#      return (x - np.min(x)) / (np.max(x) - np.min(x)) * (b - a) + a

# import pyaudio
# import matplotlib.pyplot as plt
# import struct

# fs = 44100
# sound_duration = 1
# p = pyaudio.PyAudio()
# stream = p.open(format = pyaudio.paFloat32, channels = 2, rate = fs, output = True)

# outbuf = np.random.normal(loc=0, scale=1, size=int(float(sound_duration)*fs))


# dur = int(fs * float(sound_duration))
# theta_1 = 0.0
# incr_theta_1 = 440 * 2 * np.pi / fs # frequency increment normalized for sample rate

# theta_2 = 0.0
# incr_theta_2 = 220 * 2 * np.pi / fs # frequency increment normalized for sample rate
# for i in range(dur):
#     outbuf[i] = np.sin(theta_1)/2 + np.sin(theta_2)/2
    
#     theta_1 += incr_theta_1
#     theta_2 += incr_theta_2

# data = b''.join(struct.pack('f', samp) for samp in outbuf) # must pack the binary data

# stream.write(data)
