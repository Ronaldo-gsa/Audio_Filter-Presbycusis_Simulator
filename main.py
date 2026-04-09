# Project - Filter Audio Analysis
# Ronaldo Araújo

# ============================================
# region 1. Libraries

import numpy as np
import matplotlib.pyplot as plt # Plot graph
from scipy.io import wavfile # I/O to wavfiles
from scipy import signal # Filters
from scipy.fft import fft, fftfreq # FFT
#endregion


# ============================================
# region 2. Read audio file

audio_path = 'assets/audio_files/5th_symphony.wav'

order = 4
freq_cut_off = 1500

samplerate, data = wavfile.read(audio_path)
# endregion


# ============================================
# region 3. Generate mono audio

if (len(data.shape)==2):
    data_mono = data[:,0]
elif (len(data.shape) == 1):
    data_mono = data
else:
    print("Error! Too many audio channels")

max_int16 = np.iinfo(data_mono.dtype).max
data_mono_float = data_mono.astype(np.float64) / max_int16
# endregion


# ============================================
# region 4. FILTERS

b, a = signal.butter(order,freq_cut_off,btype='lowpass',analog=False,fs=samplerate)

data_filtered = signal.filtfilt(b, a, data_mono_float)

data_filtered_normalized = np.int16(data_filtered * (np.iinfo(np.int16).max / np.max(np.abs(data_filtered))))

filtered_file_path = f'filtered_audio_{freq_cut_off}Hz.wav'
wavfile.write(filtered_file_path, samplerate, data_filtered_normalized)
# endregion


# ============================================
# region 5. Calculate FFT

number_samples = len(data_mono_float)
period = 1.0 / samplerate

mono_fft = fft(data_mono_float) 
sample_freq = fftfreq(number_samples, d=period) 

mono_fft_mag = np.abs(mono_fft[:number_samples//2])
y_mono_fft = (2.0/number_samples) * mono_fft_mag 
x_mono_fft = sample_freq[:number_samples//2]

filtered_fft = fft(data_filtered)
filtered_fft_mag = np.abs(filtered_fft[:number_samples//2])
y_filtered_fft = (2.0/number_samples) * filtered_fft_mag
x_filtered_fft = sample_freq[:number_samples//2]
# endregion


# ============================================
# region 6. PLOT GRAPH

plt.plot(
    x_mono_fft,
    y_mono_fft,
    label='Original audio',
    color='blue',
    linewidth=2
) 

plt.plot(
    x_filtered_fft,
    y_filtered_fft,
    label=f'Filtered audio at {freq_cut_off}Hz',
    color='red',
    linewidth=1
) 

plt.title(f"FFT of {audio_path}")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude Normalized")
plt.grid()
plt.legend() 
plt.xlim(0, 4000) 
plt.axvline(freq_cut_off, color='green', linestyle='--')
plt.show()