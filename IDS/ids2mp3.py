import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.interpolate import interp1d

# Read CSV file
csv_file = r"/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/IDS/IDS traces/cryostat/openAirMusic.csv"

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Extract frequency
header = data[0]
frequency = float(header[1].split(';')[1]) * 1000  # Convert kHz to Hz

# Extract time and displacement data
time_data = []
displacement_data = []
for row in data[6:]:
    try:
        time = float(row[0].split(';')[0])
        displacement = float(row[1].split(';')[0])
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

# Write audio to file
output_file = "audio_trace.wav"
write(output_file, sample_rate, audio_signal)

# Plot the displacement trace
plt.plot(time_interpolated, displacement_interpolated)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Displacement vs Time')
plt.grid(True)
plt.show()

print("Audio trace saved as:", output_file)
