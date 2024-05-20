import matplotlib
matplotlib.use('TkAgg')
import os
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from datetime import datetime, timedelta

#folder_path = 'Acceleration Data'
folder_path = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerTest005'

def load_flac_file(filepath):
    # Load FLAC file
    data, samplerate = sf.read(filepath)
    if data.ndim > 1:
        data = data[:, 0]  # Select only the Left channel
    return data, samplerate

def compute_fft(data, samplerate):
    # Compute the FFT
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(len(data), d=1 / samplerate)
    return fft_freq, np.abs(fft_data)

def plot_fft(frequencies, amplitudes, offset_minutes, label):
    # Normalize amplitudes
    normalized_amplitudes = amplitudes * (1 / 1706)  # Normalize as per the specified sensitivity factor

    # Filter frequencies between 0 and 8000 Hz
    mask = (frequencies > 1) & (frequencies <= 8000)  # Adjusted to exclude zero frequency from log scale
    filtered_freq = frequencies[mask]
    filtered_amps = normalized_amplitudes[mask]

    plt.plot(filtered_freq, filtered_amps + offset_minutes, label=label)

def main():
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.flac')])

    base_time = None
    for file_name in file_names:
        print(file_name)  # Print the file name for debugging
        # Extract time from file name
        date_str = file_name.split('.')[0]
        file_datetime = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

        if base_time is None:
            base_time = file_datetime

        # Calculate offset in minutes from the base time
        offset_minutes = (file_datetime - base_time).total_seconds() / 360000  # Adjusted to make offsets visible

        # Load data
        file_path = os.path.join(folder_path, file_name)
        data, samplerate = load_flac_file(file_path)

        # Compute FFT
        frequencies, amplitudes = compute_fft(data, samplerate)

        # Plot FFT
        plot_fft(frequencies, amplitudes, offset_minutes, file_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (offset by minutes)')
    plt.title('FFT of Acceleration Data')
    plt.legend()
    plt.gca().set_xscale("log")  # Set the x-axis to a logarithmic scale
    plt.show()

if __name__ == "__main__":
    main()
