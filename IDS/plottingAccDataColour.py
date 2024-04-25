import matplotlib

matplotlib.use('TkAgg')
import os
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from datetime import datetime


def load_flac_file(filepath):
    data, samplerate = sf.read(filepath)
    if data.ndim > 1:
        data = data[:, 0]  # Select only the Left channel
    return data, samplerate


def compute_fft(data, samplerate):
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(len(data), d=1 / samplerate)
    return fft_freq, np.abs(fft_data)


def main():
    folder_path = 'Acceleration Data'
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.flac')])

    base_time = None
    all_amplitudes = []
    times = []

    for file_name in file_names:
        date_str = file_name.split('.')[0]
        file_datetime = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

        if base_time is None:
            base_time = file_datetime

        offset_minutes = (file_datetime - base_time).total_seconds() / 60

        file_path = os.path.join(folder_path, file_name)
        data, samplerate = load_flac_file(file_path)

        frequencies, amplitudes = compute_fft(data, samplerate)

        # Normalize and filter data
        amplitudes = amplitudes * (1 / 1706)
        mask = (frequencies > 1) & (frequencies <= 8000)
        frequencies = frequencies[mask]
        amplitudes = amplitudes[mask]

        all_amplitudes.append(amplitudes)
        times.append(offset_minutes)

    # Convert lists to numpy arrays
    frequencies = frequencies
    all_amplitudes = np.array(all_amplitudes)
    times = np.array(times)

    # Create a meshgrid for time and frequency
    T, F = np.meshgrid(times, frequencies)

    plt.figure(figsize=(10, 8))
    plt.pcolormesh(T, F, all_amplitudes.T, shading='auto')
    plt.colorbar(label='Normalized Amplitude')
    plt.xlabel('Time (minutes from start)')
    plt.ylabel('Frequency (Hz)')
    plt.title('FFT of Acceleration Data Over Time')
    plt.yscale('log')
    plt.show()


if __name__ == "__main__":
    main()
