import librosa
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def plot_spectrogram(filepath, window_size=1, hop_size=1):
    """
    Plots the spectrogram of an MP3 file with a sliding window and frequency capped at 8000 Hz.

    Args:
        filepath: Path to the MP3 file.
        window_size: Size of the window in seconds for FFT calculation (default: 10).
        hop_size: Size of the hop between successive windows in seconds (default: 5).
    """
    # Load audio file
    y, sr = librosa.load(filepath, sr=None)

    # Calculate the number of samples per window and hop size
    frame_size = int(sr * window_size)
    hop_length = int(sr * hop_size)

    # Compute the spectrogram with specified parameters
    S = np.abs(librosa.stft(y, n_fft=frame_size, hop_length=hop_length, win_length=frame_size))

    # Convert amplitude spectrum to dB-scaled spectrum
    D = librosa.amplitude_to_db(S, ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))

    cmap = 'inferno'  # 'inferno' is good for showing extreme differences
    norm = colors.Normalize(vmin=-60, vmax=0)  # Adjust dB range to focus on relevant parts

    # Use the librosa.display.specshow() function with frequency axis limited to 8000 Hz
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', hop_length=hop_length, fmax=8000, cmap=cmap, norm=norm)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of ' + 'pumpingDown')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.ylim([0, 1024])
    plt.xlim([0, 900])
    plt.tight_layout()
    plt.show()

# Replace with the path to your MP3 file
filepath = "/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/pumpingDown.mp3"
plot_spectrogram(filepath)
