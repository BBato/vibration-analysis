import time
import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fftpack import fft

#Prompt user for file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Two Column CSV","*.csv")])
print(file_path)

#Load Data (assumes two column array
tic = time.process_time()
[t, x] = np.genfromtxt(file_path,delimiter=',', unpack=True, dtype=float, encoding='utf-8-sig')
toc = time.process_time()
print("Load Time:",toc-tic)

#Determine variables
N = np.int(np.prod(t.shape))#length of the array
Fs = 1/(t[1]-t[0]) 	#sample rate (Hz)
T = 1/Fs
print("# Samples:",N)

#Plot Data
tic = time.process_time()
plt.figure(1)  
plt.plot(t, x)
plt.xlabel('Time (seconds)')
plt.ylabel('Accel (g)')
plt.title(file_path)
plt.grid()
toc = time.process_time()
print("Plot Time:",toc-tic)

#Compute RMS and Plot
tic = time.process_time()
w = int(np.ceil(Fs)); #width of the window for computing RMS
steps = int(np.ceil(N/w)); #Number of steps for RMS
t_RMS = np.zeros((steps,1)); #Create array for RMS time values
x_RMS = np.zeros((steps,1)); #Create array for RMS values
for i in range (0, steps):
	t_RMS[i] = np.mean(t[(i*w):((i+1)*w)])
	x_RMS[i] = np.sqrt(np.mean(x[(i*w):((i+1)*w)]**2));  
plt.figure(2)  
plt.plot(t_RMS, x_RMS)
plt.xlabel('Time (seconds)')
plt.ylabel('RMS Accel (g)')
plt.title('RMS')
plt.grid()
toc = time.process_time()
print("RMS Time:",toc-tic)

#Compute and Plot FFT
tic = time.process_time()
plt.figure(3)
xf = np.linspace(0.0, 1.0/(2.0*T), int(N/2))
yf = fft(x)
plt.plot(xf, 2.0/N * np.abs(yf[0:int(N/2)]))
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Accel (g)')
plt.title('FFT')
toc = time.process_time()
print("FFT Time:",toc-tic)

# Compute and Plot Spectrogram
tic = time.process_time()
plt.figure(4)  
[f, t2, Sxx] = signal.spectrogram(x, int(Fs), nperseg = int(Fs/4))
plt.pcolormesh(t2, f, np.log(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram')
toc = time.process_time()
print("Spectrogram Time:",toc-tic)
plt.show()
