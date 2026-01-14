# Project - Filter Audio Analysis
# Ronaldo Gonçalves S. Araújo
# Github: 

# ============================================
# region 1. Libraries
import numpy as np
import matplotlib.pyplot as plt # Plot graph
from scipy.io import wavfile # I/O to wavfiles
from scipy import signal # Filters
from scipy.fft import fft, fftfreq # Import FFT
#endregion


# ============================================
# region 2. Read audio file

# audio_path = 'audio_files/arcade.wav'
# audio_path = 'audio_files/Sputnik.wav'
# audio_path = 'audio_files/15kHz.wav'
# audio_path = 'audio_files/Symp_5.wav'
audio_path = 'audio_files/Symp_5_reduced.wav'

samplerate, data = wavfile.read(audio_path)
# endregion


# ============================================
# region 3. Generate mono audio
if (len(data.shape)==2):
    data_mono = data[:,0]
    # print("stereo")
elif (len(data.shape) == 1):
    data_mono = data
    # print("mono")
else:
    print("Error! Too many audio channels")

max_int16 = np.iinfo(data_mono.dtype).max
data_mono_float = data_mono.astype(np.float64) / max_int16
data_mono_normalized_int16 = np.int16(data_mono_float * max_int16)

mono_file_path = 'mono_file_normalized.wav'
wavfile.write(mono_file_path, samplerate, data_mono_normalized_int16)
# endregion


# ============================================
# region 4. FILTERS AND TINNITUS SIMULATION
# 4.1 Filtro Passa-Baixa (Simulando perda auditiva severa)
order = 8
freq_cut_off = 800 

b, a = signal.butter(order, freq_cut_off, btype='lowpass', analog=False, fs=samplerate)
data_filtered = signal.filtfilt(b, a, data_mono_float)

# 4.2 Geração do Zumbido Modulado com Fade-in (Parâmetros Solicitados)
tinnitus_center_freq = 3500  # Frequência de compensação cerebral
tinnitus_amplitude = 0.001   # Volume muito sutil
deviation = 60               # Oscilação de 60Hz para cima/baixo
mod_speed = 0.2              # Oscilação lenta (uma a cada 5 segundos)
fade_duration_sec = 5.0      # Tempo de subida gradual do ruído

t = np.linspace(0, len(data_filtered) / samplerate, len(data_filtered), endpoint=False)

# Cálculo da fase para frequência variável (vibrato orgânico)
vibrato = deviation * np.sin(2 * np.pi * mod_speed * t)
phase = 2 * np.pi * (tinnitus_center_freq * t + np.cumsum(vibrato) / samplerate)
zumbido_base = tinnitus_amplitude * np.sin(phase)

# Criar rampa de volume (Fade-in linear)
num_fade_samples = int(fade_duration_sec * samplerate)
fade_envelope = np.ones(len(data_filtered))
fade_envelope[:num_fade_samples] = np.linspace(0, 1, num_fade_samples)

zumbido_com_fade = zumbido_base * fade_envelope

# 4.3 Mixagem e Normalização
data_combined = data_filtered + zumbido_com_fade

# Normalização Final
peak = np.max(np.abs(data_combined))
if peak > 0:
    data_final = data_combined / peak
else:
    data_final = data_combined

# Conversão para 16-bit PCM
data_final_int16 = np.int16(data_final * 32767)

output_path = f'simulacao_beethoven_3500Hz_sutil.wav'
wavfile.write(output_path, samplerate, data_final_int16)

print(f"Arquivo gerado com sucesso: {output_path}")
# endregion

# ============================================
# region 5. Calculate FFT
number_samples = len(data_mono_float)
period = 1.0 / samplerate

# FFT Audio Mono
mono_fft = fft(data_mono_float) # array de complexos
sample_freq = fftfreq(number_samples, d=period) # retorna frequencias fundamentais dos pontos de fft

mono_fft_mag = np.abs(mono_fft[:number_samples//2]) # Only positive freq and magnitude of complex numbers
y_mono_fft = (2.0/number_samples) * mono_fft_mag #Normalization
x_mono_fft = sample_freq[:number_samples//2]

# FFT Audio Filtrado
filtered_fft = fft(data_filtered)
filtered_fft_mag = np.abs(filtered_fft[:number_samples//2])
y_filtered_fft = (2.0/number_samples) * filtered_fft_mag
x_filtered_fft = sample_freq[:number_samples//2]
# endregion


# ============================================
# region 6. PLOT GRAPH
# Define o tamanho da figura (Largura, Altura) em polegadas
plt.figure(figsize=(15, 6)) 

plt.plot(
    x_mono_fft,
    y_mono_fft,
    label='Original audio',
    color='blue',
    linewidth=1.5,
    alpha=0.6 # Reduzi a opacidade para facilitar a comparação
) 

plt.plot(
    x_filtered_fft,
    y_filtered_fft,
    label=f'Filtered audio at {freq_cut_off}Hz',
    color='red',
    linewidth=1.5
) 

plt.title(f"FFT of 5th symphony Beethoven")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude Normalized")
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend() 
plt.xlim(0, 3000) # Aumentei um pouco para ver o pico de 3500Hz do zumbido

# Linha indicando o corte do filtro
plt.axvline(freq_cut_off, color='green', linestyle='--', label='Cut-off frequency')


plt.tight_layout() # Ajusta automaticamente as margens para não cortar os rótulos
plt.show()

# # O limite máximo é a Frequência de Nyquist (samplerate / 2)
# # Muitas vezes, um limite menor (ex: 5000 Hz) é mais útil para áudio.
# # Max_f = samplerate / 2
#endregion

# # ============================================
# # region 7. SPECTROGRAM
# frequencies, times, spectrogram = signal.spectrogram(data_final, samplerate)

# plt.figure(figsize=(10, 5))
# plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='gouraud', cmap='magma')

# plt.title('Espectrograma: Simulação de Beethoven')
# plt.ylabel('Frequência [Hz]')
# plt.xlabel('Tempo [seg]')
# plt.ylim(0, 5000) # Foco na área do filtro e do zumbido
# plt.colorbar(label='Intensidade [dB]')
# plt.tight_layout()
# plt.show()
# # endregion