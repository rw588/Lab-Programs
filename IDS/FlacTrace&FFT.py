import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from datetime import datetime
from scipy.integrate import cumtrapz
from scipy.signal import detrend

def load_wav_file(filepath):
    # Load WAV file
    data, samplerate = sf.read(filepath)
    if data.ndim > 1:
        data = data[:, 0]  # Select only the Left channel
    return data, samplerate

def compute_fft(data, samplerate):
    # Compute the FFT
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(len(data), d=1 / samplerate)
    return fft_freq, np.abs(fft_data)

def plot_fft(frequencies, amplitudes, ax, label):
    # Normalize amplitudes
    normalized_amplitudes = amplitudes * (1 / 1706)  # Normalize as per the specified sensitivity factor

    # Filter frequencies between 0 and 8000 Hz
    mask = (frequencies > 1) & (frequencies <= 8000)  # Adjusted to exclude zero frequency from log scale
    filtered_freq = frequencies[mask]
    filtered_amps = normalized_amplitudes[mask]

    ax.plot(filtered_freq, filtered_amps, label=label)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude')
    ax.set_title('FFT of Audio Signal/ (arb.)')
    ax.set_xlim([0, 3000])
    ax.legend()

def plot_waveform(time, acceleration, ax, std_dev, max_val):
    ax.plot(time, acceleration)
    ax.set_title(f'10 ms Segment of Audio Waveform\nStandard Deviation: {std_dev:.4f}\nOverall max: {max_val:.4f}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Acceleration / (arb.)')
    ax.grid(True)

def main():
    # Specify the file path
    file_path = 'Data/840mK.wav'
    #file_path = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronDataDeNoisedAdv005/2024-05-08_09-30-26.flac'
    #file_path = 'Data/coldishNoPulseNoTurbo.wav'
    
    # Load data
    trace, samplerate = load_wav_file(file_path)
    data = trace * 10 * 0.564075  # to convert V to ms-2

    # Compute FFT
    frequencies, amplitudes = compute_fft(data, samplerate)

    # Extract a 10 ms segment
    duration_in_seconds = 0.01
    samples_to_extract = int(samplerate * duration_in_seconds)
    acceleration = detrend(data[:samples_to_extract])
    time = np.linspace(0, duration_in_seconds, num=samples_to_extract, endpoint=False)

    # Calculate the standard deviation and maximum value of the segment's amplitude
    std_dev = np.std(acceleration)
    max_val = np.max(data)
    print(f"Standard Deviation of Acceleration: {std_dev:.4f}")
    print(f"Maximum Value of Acceleration: {max_val:.4f}")

    # Plot waveform and FFT
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot waveform
    plot_waveform(time, acceleration, ax1, std_dev, max_val)

    # Plot FFT
    plot_fft(frequencies, amplitudes, ax2, 'FFT')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
