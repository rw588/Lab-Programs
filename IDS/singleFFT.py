import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from datetime import datetime

#file_path = "/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronData/2024-05-07_11-50-27.flac"
    
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

def plot_fft(frequencies, amplitudes, label):
    # Normalize amplitudes
    normalized_amplitudes = amplitudes * (1 / 1706)  # Normalize as per the specified sensitivity factor

    # Filter frequencies between 0 and 8000 Hz
    mask = (frequencies > 1) & (frequencies <= 8000)  # Adjusted to exclude zero frequency from log scale
    filtered_freq = frequencies[mask]
    filtered_amps = normalized_amplitudes[mask]

    plt.plot(filtered_freq, filtered_amps, label=label)

def main():
    # Directly specify the file or use a dialog to select a file
    
    # Load data
    trace, samplerate = load_flac_file(file_path)
    data = trace * 10 * 0.564075 #to convert V to ms-2


    # Compute FFT
    frequencies, amplitudes = compute_fft(data, samplerate)

    # Extract date from file path for labeling purposes
    file_name = file_path.split('/')[-1]
    date_str = file_name.split('.')[0]
    file_datetime = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

    # Plot FFT
    plot_fft(frequencies, amplitudes, file_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Acceleration/ ms-2')
    plt.title('FFT of Single Acceleration File')
    plt.legend()
    plt.xlim([0, 3000])
    #plt.gca().set_xscale("log")  # Set the x-axis to a logarithmic scale
    plt.show()

if __name__ == "__main__":
    main()
