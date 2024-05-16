import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import soundfile as sf

# Membaca file audio menggunakan soundfile
data, sampling_rate = sf.read('./sample/Data sample 1.wav')

# Jika stereo, konversi ke mono dengan rata-rata dua channel
if len(data.shape) == 2:
    data = np.mean(data, axis=1)

# Normalisasi data
data = data / np.max(np.abs(data))

# Kecepatan suara dalam udara (m/s)
speed_of_sound = 343.0

# Kecepatan sumber (positif jika mendekat, negatif jika menjauh)
source_speed = 20.0  # m/s, contoh nilai

# Kecepatan pendengar (positif jika mendekat, negatif jika menjauh)
listener_speed = 0.0  # m/s, contoh nilai

# Fungsi untuk menghitung frekuensi terdeteksi berdasarkan efek Doppler
def doppler_effect(frequency, source_speed, listener_speed, speed_of_sound):
    return frequency * ((speed_of_sound + listener_speed) / (speed_of_sound - source_speed))

# Menghitung FFT
N = len(data)
T = 1.0 / sampling_rate
yf = fft(data)
xf = fftfreq(N, T)[:N//2]

# Mengambil magnitudo spektrum
yf_magnitude = np.abs(yf[:N//2])

# Menyesuaikan frekuensi berdasarkan efek Doppler
xf_doppler = doppler_effect(xf, source_speed, listener_speed, speed_of_sound)

# Plot spektrum frekuensi sebelum dan sesudah efek Doppler
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(xf, yf_magnitude)
plt.title('Spektrum Frekuensi Asli')
plt.xlabel('Frekuensi (Hz)')
plt.ylabel('Magnitudo')

plt.subplot(2, 1, 2)
plt.plot(xf_doppler, yf_magnitude)
plt.title('Spektrum Frekuensi dengan Efek Doppler')
plt.xlabel('Frekuensi (Hz)')
plt.ylabel('Magnitudo')

plt.tight_layout()
plt.show()


# Menentukan frekuensi terendah dan tertinggi setelah efek Doppler
threshold = 0.1 * np.max(yf_magnitude)  # Contoh threshold
indices = np.where(yf_magnitude > threshold)[0]
min_freq_doppler = xf_doppler[indices[0]]
max_freq_doppler = xf_doppler[indices[-1]]

# Menyimpan hasil ke dalam dataframe
df = pd.DataFrame({
    'Frekuensi Terendah': [xf[indices[0]], xf_doppler[indices[0]]] + [None]*(len(yf_magnitude)-2),
    'Frekuensi Tertinggi': [xf[indices[-1]], xf_doppler[indices[-1]]] + [None]*(len(yf_magnitude)-2),
    'FFT': yf_magnitude
})

# Menyimpan dataframe ke dalam file Excel
df.to_excel('hasil_analisis_audio.xlsx', index=False)

print(f"Frekuensi terendah dengan efek Doppler: {min_freq_doppler:.2f} Hz")
print(f"Frekuensi tertinggi dengan efek Doppler: {max_freq_doppler:.2f} Hz")
