import matplotlib

matplotlib.use('TkAgg')
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import soundfile as sf
from datetime import datetime
from matplotlib.colors import LogNorm

#folder_path = 'Acceleration Data'
#folder_path = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronDataDeNoised005'
folder_path = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronDataDeNoisedAdv005'

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
#    folder_path = 'Acceleration Data'
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.flac')])

    base_time = None
    all_amplitudes = []
    times = []
    datetimes = []
    max_length = 0  # Variable to store the maximum length

    # First, determine the maximum length of the amplitudes
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        data, samplerate = load_flac_file(file_path)
        frequencies, amplitudes = compute_fft(data, samplerate)
        mask = (frequencies > 1) & (frequencies <= 8000)
        if np.sum(mask) > max_length:
            max_length = np.sum(mask)

    # Then, process files again to normalize and pad amplitudes
    for file_name in file_names:
        date_str = file_name.split('.')[0]
        file_datetime = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
        datetimes.append(file_datetime)

        if base_time is None:
            base_time = file_datetime

        offset_minutes = (file_datetime - base_time).total_seconds() / 60

        file_path = os.path.join(folder_path, file_name)
        data, samplerate = load_flac_file(file_path)

        frequencies, amplitudes = compute_fft(data, samplerate)
        amplitudes = amplitudes * (1 / 1706)
        mask = (frequencies > 1) & (frequencies <= 8000)
        frequencies = frequencies[mask]
        amplitudes = amplitudes[mask]

        # Pad the amplitudes array to have the same length as max_length
        if len(amplitudes) < max_length:
            amplitudes = np.pad(amplitudes, (0, max_length - len(amplitudes)), 'constant')

        all_amplitudes.append(amplitudes)
        times.append(offset_minutes)

    all_amplitudes = np.array(all_amplitudes)
    times = np.array(times)
    datetimes = np.array(datetimes)
    frequencies = np.linspace(1, 8000, max_length)  # Assuming a linear distribution

    T, F = np.meshgrid(datetimes, frequencies)

    plt.figure(figsize=(10, 8))

# Define color limits for the color scale
    vmin = 1e-6  # Minimum value for logarithmic scale (should be > 0)
    vmax = 0.0001  # Maximum value
# Assuming T and F are the arrays for Time and Frequency, and all_amplitudes.T is the matrix of amplitudes
    c = plt.pcolormesh(T, F, all_amplitudes.T, shading='auto', norm=LogNorm(vmin=vmin, vmax=vmax))
    plt.colorbar(c, label='Normalized Amplitude')

    plt.xlabel('Time')
    plt.ylabel('Frequency (Hz)')
    plt.title('FFT of Acceleration Data Over Time')

    plt.ylim([0, 3000])
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    main()
