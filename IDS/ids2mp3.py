import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.interpolate import interp1d
from scipy.signal import iirnotch, lfilter

# Read CSV file
csv_file = r"/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/IDS/IDS traces/cryostat/openAirMusic.csv"

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Extract time and displacement data
time_data = []
displacement_data = []
for row in data[6:]:
    try:
        time = float(row[0].split(';')[0])
        displacement = float(row[0].split(';')[1])
        time_data.append(time)
        displacement_data.append(displacement)
    except ValueError:
        pass

# Convert picometers to meters
displacement_data = np.array(displacement_data) * 1e-12

# Subtract the initial displacement as baseline
baseline = displacement_data[0]
displacement_data -= baseline

# Interpolate to get smooth displacement values
interp_func = interp1d(time_data, displacement_data, kind='cubic')
time_interpolated = np.linspace(min(time_data), max(time_data), num=len(time_data)*10)
displacement_interpolated = interp_func(time_interpolated)

# Generate audio signal
sample_rate = 44100  # Sample rate in Hz
duration = max(time_interpolated)  # Duration in seconds
t = np.linspace(0, duration, int(sample_rate * duration))
audio_signal = np.interp(t, time_interpolated, displacement_interpolated)

# Normalize audio signal
audio_signal /= np.max(np.abs(audio_signal))

# Apply notch filter to remove frequencies around 300 Hz
f0 = 300.0  # Frequency to be removed from the signal (Hz)
nyquist = 0.5 * sample_rate
w0 = f0 / nyquist
Q = 30.0    # Quality factor
b, a = iirnotch(w0, Q)
audio_signal_filtered = lfilter(b, a, audio_signal)

# Write filtered audio to file
output_file = "audio_trace_filtered.wav"
write(output_file, sample_rate, audio_signal_filtered)

# Plot the filtered audio signal
plt.figure(figsize=(10, 5))
plt.plot(t, audio_signal_filtered)
plt.title('Filtered Audio Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# Compute FFT of the filtered audio signal
n = len(audio_signal_filtered)
frequencies = np.fft.rfftfreq(n, d=1/sample_rate)
fft_values = np.abs(np.fft.rfft(audio_signal_filtered))

# Plot FFT of the filtered audio signal
plt.figure(figsize=(10, 5))
plt.plot(frequencies, fft_values)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT of Filtered Audio Signal')
plt.grid(True)
plt.show()

print("Filtered audio trace saved as:", output_file)
