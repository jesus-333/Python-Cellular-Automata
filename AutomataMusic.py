#%% Imports

import numpy as np
import matplotlib.pyplot as plt
import pyaudio

#%%

def readFrequnecyFromFile():
    freq_list = []
    
    # Read the files and return the element as a list of string
    with open('notes_frequency.txt') as f:
        tmp_data = f.readlines()
        
    # Convert the list of string in a list of float
    for freq in tmp_data: freq_list.append(float(freq))
    
    return freq_list


def rescale(x, a = 0, b = 1):
     return (x - np.min(x)) / (np.max(x) - np.min(x)) * (b - a) + a
 
    
#%% 

class AntsMusic():
    
    def __init__(self, width, length):
        a = 1;



#%%
import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudioPyAudio = pyaudio.PyAudio     #initialize pyaudio
p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 8000       # sampling rate, Hz, must be integer
duration = 3.0   # in seconds, may be float
f1 = 440.0        # sine frequency, Hz, may be float
f2 = 880.0

# generate samples, note conversion to float32 array
samples_1 = (np.sin(2*np.pi*np.arange(fs*duration)* f1 /fs)).astype(np.float32)
samples_2 = (np.sin(2*np.pi*np.arange(fs*duration)* f2 /fs)).astype(np.float32)
samples_3 = (np.sin(2*np.pi*np.arange(fs*duration)* 220 /fs)).astype(np.float32)
samples_4 = (np.sin(2*np.pi*np.arange(fs*duration)* 523.25 /fs)).astype(np.float32)

samples = samples_1 + samples_2 + samples_3 + samples_4

plt.plot(samples_1)
plt.plot(samples_2)
plt.plot(samples)
plt.xlim([0, 200])

samples = samples_2

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
# stream.write(samples_1)
# stream.write(samples_2)
# stream.write(rescale(samples_1))
# stream.write(rescale(samples_1 + samples_2))
stream.write(rescale(samples_1 + samples_2 + samples_3))
stream.write(rescale(samples_1 + samples_2 + samples_3 + samples_4))

stream.stop_stream()
stream.close()

p.terminate()



#%%

import math
import wave
import struct


def synthComplex(freq=[440],coef=[1], datasize=10000, fname="test.wav"):
    frate = 44100.00  
    amp=8000.0 
    sine_list=[]
    for x in range(datasize):
        samp = 0
        for k in range(len(freq)):
            samp = samp + coef[k] * math.sin(2*math.pi*freq[k]*(x/frate))
        sine_list.append(samp)
    wav_file=wave.open(fname,"w")
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes=datasize
    comptype= "NONE"
    compname= "not compressed"
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    for s in sine_list:
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    wav_file.close()
    
    return sine_list

a = synthComplex([440,880], [1, 1], 30000, "tone.wav")
