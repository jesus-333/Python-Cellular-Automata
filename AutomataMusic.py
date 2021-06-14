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
 
    
#%%  Versione 1 - Ants music

class AntsMusicV1():
    
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
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paFloat32, channels = 2, rate = self.fs, output = True)
        
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
        sine_wave = rescale(sine_wave)
        
        # Reproduce sound
        self.stream.write(sine_wave)
        # stream.stop_stream()
        # stream.close()
        
        # p.terminate()
        
        return sine_wave
    
#%%  Versione 2 - Ants music    

class AntsMusicV2():
    
    def __init__(self, width, height, sound_duration = 1, fs = 44100, channels = 1, ref_freq = 440):
        self.width, self.height = width, height
        self.fs = fs
        self.sound_duration = sound_duration
        
        # Read the frequency list
        self.freq_list = readFrequnecyFromFile();
        
        # Find the minimum and maximum exponent
        self.min_exp, self.max_exp = self.findExponent(ref_freq)
        
        # Sound map creation
        self.sound_map = self.createSoundMap(sound_duration = sound_duration, fs = fs)
        
        # 
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paFloat32, channels = 2, rate = self.fs, output = True)
        
        
    def findExponent(self, ref_freq):
        min_freq = np.min(self.freq_list)
        max_freq = np.max(self.freq_list)
        
        n_min = 0
        n_max = 0
        
        end_min = False
        end_max = False
        
        while(True):
            tmp_min_freq = ref_freq * 2 ** (n_min / 12)
            tmp_max_freq = ref_freq * 2 ** (n_max / 12)
            
            if(abs(tmp_min_freq - min_freq) <= 0.1): end_min = True
            else: n_min -= 1
            
            if(abs(tmp_max_freq - max_freq) <= 0.1): end_max = True
            else: n_max += 1
            
            if(end_min and end_max): break
        
        return n_min, n_max
            
            
                
    def createSoundMap(self, sound_duration = 1, fs = 44100, ref_freq = 440):
        """
        Create a matrix with the same size of the Langton Ants Cellular Automata Grid.
        At each element of the grid corresponding a sine wave.

        """
        
        # Matrix creation
        sound_map = np.zeros((self.height, self.width))
        idx_freq = 0
        
        for i in range(self.height):
            n = i
            
            for j in range(self.width):
                # Exponent check. If it is bigger than max set it to min
                if(n >= self.max_exp): n = self.min_exp
                
                # Evaluate frequency for the current cell
                tmp_freq = ref_freq * 2 ** (n / 12)
                
                # Advance frequency exponent
                n += 1
                
                # Save frequency into the cell
                sound_map[i, j] = tmp_freq
            
        return sound_map
    
    
    def sound(self, list_of_ants):
        sine_wave = np.zeros(int(self.fs * self.sound_duration))
        for ant in list_of_ants:
            i, j = ant['position']
            
            sine_wave += (np.sin(2*np.pi*np.arange(self.fs * self.sound_duration)* self.sound_map[i, j]/self.fs)).astype(np.float32)
        
        # Rescale in 0-1 range
        sine_wave = rescale(sine_wave)
        
        # Reproduce sound
        self.stream.write(sine_wave)
        # stream.stop_stream()
        # stream.close()
        
        # p.terminate()
        
        return sine_wave