#%% Imports

import numpy as np
import matplotlib.pyplot as plt
import pyaudio

#%%

def readFrequnecyFromFile():
    freq_list = []
    
    # Read the files and return the element as a list of string
    with open('notes_frequency_2.txt') as f:
        tmp_data = f.readlines()
        
    # Convert the list of string in a list of float
    for freq in tmp_data: freq_list.append(float(freq))
    
    return freq_list


def rescale(x, a = 0, b = 1):
     return (x - np.min(x)) / (np.max(x) - np.min(x)) * (b - a) + a
 
    
#%% 

class AntsMusic():
    
    def __init__(self, width, height, sound_duration = 1, fs = 44100, channels = 1):
        self.width, self.height = width, height
        self.fs = fs
        self.sound_duration = sound_duration
        
        # Read the frequency list
        self.freq_list = readFrequnecyFromFile();
        
        # Find the minimum and maximum exponent
        self.min_exp_list = self.min_exp()
        self.max_exp_list = self.max_exp()
        
        # Sound map creation
        self.sound_map = self.createSoundMap(sound_duration = sound_duration, fs = fs)
        
        # 
        p = pyaudio.PyAudio()
        self.stream = p.open(format = pyaudio.paFloat32, channels = 1, rate = self.fs, output = True)
        
    def min_exp(self):
        """
        Evaluate the minimum exponenent needed to obtain a frequency equal or lower to the minumum frequency in the frequency list
        For my list the minimum frequency is 16.35Hz (C0).
        
        The exponent is considered as the n in the formula new_f = f * 2 ** (n/12) where f is the current frequency analyzed

        """
        
        min_exp_list = []
        
        # Find the minimum frequency of the list (16.35Hz, C0)
        min_abs_freq = np.min(self.freq_list)
        
        for freq in self.freq_list:
            n = 0
            while(True):
                tmp_freq = freq * 2 ** (n / 12)
                
                # If the new frequency is lower than the absolute minimum save the n and stop the inner cycle. Otherwise reduce n
                if(tmp_freq <= min_abs_freq): 
                    min_exp_list.append(n)
                    break
                else:
                    n -= 1
                    
        return min_exp_list
    
    def max_exp(self):
        """
        Same as min_exp but for the max frequenc
        """
        
        max_exp_list = []
        max_abs_freq = np.max(self.freq_list)
        
        for freq in self.freq_list:
            n = 0
            while(True):
                tmp_freq = freq * 2 ** (n / 12)
                
                # print("freq = {} - max_abs_freq = {} - n = {}".format(freq, max_abs_freq, n))
                
                if(tmp_freq >= max_abs_freq): 
                    max_exp_list.append(n)
                    break
                else:
                    n += 1
                    
        return max_exp_list
                
    def createSoundMap(self, sound_duration = 1, fs = 44100):
        """
        Create a matrix with the same size of the Langton Ants Cellular Automata Grid.
        At each element of the grid corresponding a sine wave.

        Returns
        -------
        None.

        """
        
        # Matrix creation
        sound_map = np.zeros((self.height, self.width))
        idx_freq = 0
        
        for i in range(self.height):
            current_freq = self.freq_list[idx_freq]
            min_exp_current_freq = self.min_exp_list[idx_freq]
            max_exp_current_freq = self.max_exp_list[idx_freq]
            n = 0
            
            for j in range(self.width):
                # Exponent check. If it is bigger than max set it to min
                if(n >= max_exp_current_freq): n = min_exp_current_freq
                
                # Evaluate frequency for the current cell
                tmp_freq = current_freq * 2 ** (n / 12)
                
                # Advance frequency exponent
                n += 1
                
                # Save frequency into the cell
                sound_map[i, j] = tmp_freq
                
                # Notes that even with a matrix 800 x 400 you need to much space to save the already precomputed sinewave
                    

            # Advance the frequency index
            idx_freq += 1
            
            # Check the frequency index
            if(idx_freq >= len(self.freq_list)): idx_freq = 0 
            
        return sound_map
    
    
    def sound(self, list_of_ants):
        

        
        sine_wave = np.zeros(int(self.fs * self.sound_duration))
        for ant in list_of_ants:
            i, j = ant['position']
            
            sine_wave += (np.sin(2*np.pi*np.arange(self.fs * self.sound_duration)* self.sound_map[i, j]/self.fs)).astype(np.float32)
        
        # Rescale in 0-1 range
        # sine_wave = rescale(sine_wave)
        
        # Reproduce sound
        self.stream.write(sine_wave)
        # stream.stop_stream()
        # stream.close()
        
        # p.terminate()



#%%
# import math        #import needed modules
# import pyaudio     #sudo apt-get install python-pyaudioPyAudio = pyaudio.PyAudio     #initialize pyaudio


# volume = 0.5     # range [0.0, 1.0]
# fs = 8000       # sampling rate, Hz, must be integer
# duration = 3.0   # in seconds, may be float
# f1 = 440.0        # sine frequency, Hz, may be float
# f2 = 880.0

# # generate samples, note conversion to float32 array
# samples_1 = (np.sin(2*np.pi*np.arange(fs*duration)* f1 /fs)).astype(np.float32)
# samples_2 = (np.sin(2*np.pi*np.arange(fs*duration)* f2 /fs)).astype(np.float32)
# samples_3 = (np.sin(2*np.pi*np.arange(fs*duration)* 220 /fs)).astype(np.float32)
# samples_4 = (np.sin(2*np.pi*np.arange(fs*duration)* 523.25 /fs)).astype(np.float32)

# samples = samples_1 + samples_2 + samples_3 + samples_4

# plt.plot(samples_1)
# plt.plot(samples_2)
# plt.plot(samples)
# plt.xlim([0, 200])

# samples = samples_2

# p = pyaudio.PyAudio()

# # for paFloat32 sample values must be in range [-1.0, 1.0]
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=fs,
#                 output=True)

# # play. May repeat with different volume values (if done interactively) 
# # stream.write(samples_1)
# # stream.write(samples_2)
# # stream.write(rescale(samples_1))
# # stream.write(rescale(samples_1 + samples_2))
# stream.write(rescale(samples_1 + samples_2 + samples_3))
# stream.write(rescale(samples_1 + samples_2 + samples_3 + samples_4))

# stream.stop_stream()
# stream.close()

# p.terminate()



# #%%

# import math
# import wave
# import struct


# def synthComplex(freq=[440],coef=[1], datasize=10000, fname="test.wav"):
#     frate = 44100.00  
#     amp=8000.0 
#     sine_list=[]
#     for x in range(datasize):
#         samp = 0
#         for k in range(len(freq)):
#             samp = samp + coef[k] * math.sin(2*math.pi*freq[k]*(x/frate))
#         sine_list.append(samp)
#     wav_file=wave.open(fname,"w")
#     nchannels = 1
#     sampwidth = 2
#     framerate = int(frate)
#     nframes=datasize
#     comptype= "NONE"
#     compname= "not compressed"
#     wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
#     for s in sine_list:
#         wav_file.writeframes(struct.pack('h', int(s*amp/2)))
#     wav_file.close()
    
#     return sine_list

# a = synthComplex([440,880], [1, 1], 30000, "tone.wav")
