import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import soundfile as sf
from mpl_toolkits.mplot3d import Axes3D

class AudioAnalyzer:
    def __init__(self, file_path, segment_duration=0.2, speed_of_sound=343.0, source_speed=20.0, listener_speed=0.0):
        self.file_path = file_path
        self.segment_duration = segment_duration
        self.speed_of_sound = speed_of_sound
        self.source_speed = source_speed
        self.listener_speed = listener_speed
        self.data, self.sampling_rate = self._read_audio_file()
        self.data = self._normalize_data()
        self.segments = self._split_into_segments()

    def _read_audio_file(self):
        data, sampling_rate = sf.read(self.file_path)
        if len(data.shape) == 2:
            data = np.mean(data, axis=1)
        return data, sampling_rate

    def _normalize_data(self):
        return self.data / np.max(np.abs(self.data))

    def _split_into_segments(self):
        segment_samples = int(self.segment_duration * self.sampling_rate)
        num_segments = int(len(self.data) / segment_samples)
        segments = [self.data[i*segment_samples:(i+1)*segment_samples] for i in range(num_segments)]
        return segments

    def doppler_effect(self, frequency):
        return frequency * ((self.speed_of_sound + self.listener_speed) / (self.speed_of_sound - self.source_speed))

    def compute_fft(self):
        fft_segments = []
        for segment in self.segments:
            N = len(segment)
            T = 1.0 / self.sampling_rate
            yf = fft(segment)
            xf = fftfreq(N, T)[:N//2]
            yf_magnitude = np.abs(yf[:N//2])
            xf_doppler = self.doppler_effect(xf)
            fft_segments.append((xf, yf_magnitude, xf_doppler))
        return fft_segments

    def analyze_frequency_ranges(self, fft_segments):
        results = []
        for xf, yf_magnitude, xf_doppler in fft_segments:
            threshold = 0.1 * np.max(yf_magnitude)
            indices = np.where(yf_magnitude > threshold)[0]
            if len(indices) > 0:
                min_freq_original = xf[indices[0]]
                max_freq_original = xf[indices[-1]]
                min_freq_doppler = xf_doppler[indices[0]]
                max_freq_doppler = xf_doppler[indices[-1]]
                results.append((min_freq_original, max_freq_original, min_freq_doppler, max_freq_doppler))
        return results

    def save_results_to_excel(self, results, filename='hasil_analisis_audio_per_segment.xlsx'):
        df = pd.DataFrame(results, columns=[
            'Frekuensi Terendah Asli',
            'Frekuensi Tertinggi Asli',
            'Frekuensi Terendah Doppler',
            'Frekuensi Tertinggi Doppler'
        ])
        df.to_excel(filename, index=False)
        print(f"Hasil analisis telah disimpan ke '{filename}'")

class Plotter:
    def __init__(self, fft_segments):
        self.fft_segments = fft_segments

    def plot_spectrum(self):
        plt.figure(figsize=(12, 6))
        for i, (xf, yf_magnitude, xf_doppler) in enumerate(self.fft_segments):
            plt.subplot(2, 1, 1)
            plt.plot(xf, yf_magnitude, label=f'Segment {i+1}')
            plt.title('Spektrum Frekuensi Asli')
            plt.xlabel('Frekuensi (Hz)')
            plt.ylabel('Magnitudo')

            plt.subplot(2, 1, 2)
            plt.plot(xf_doppler, yf_magnitude, label=f'Segment {i+1}', linestyle='--')
            plt.title('Spektrum Frekuensi dengan Efek Doppler')
            plt.xlabel('Frekuensi (Hz)')
            plt.ylabel('Magnitudo')

        plt.tight_layout()
        plt.legend()
        plt.show()

    def plot_3d_spectrum(self):
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_subplot(111, projection='3d')

        for i, (xf, yf_magnitude, xf_doppler) in enumerate(self.fft_segments):
            ax.plot(xf, np.full_like(xf, i * 0.2), yf_magnitude, color='b')
            ax.plot(xf_doppler, np.full_like(xf_doppler, i * 0.2), yf_magnitude, color='r', linestyle='--')

        ax.set_xlabel('Frekuensi (Hz)')
        ax.set_ylabel('Waktu (s)')
        ax.set_zlabel('Magnitudo')
        ax.set_title('Spektrum Frekuensi 3D dengan Efek Doppler')

        plt.show()

