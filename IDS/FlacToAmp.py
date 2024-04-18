import soundfile as sf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumtrapz
from scipy.signal import detrend
plt.rcParams.update({'font.size': 16})

# Load the FLAC file
trace, samplerate = sf.read('/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/pumpingDown.flac')

data = trace * 10 * 0.564075 #to convert V to ms-2

# Extract a 10 ms segment
# Since 10 ms = 0.01 seconds, we calculate the number of samples to extract
duration_in_seconds = 0.01
samples_to_extract = int(samplerate * duration_in_seconds)

# Assume we start extracting from the beginning
acceleration = detrend(data[:samples_to_extract])

time = np.linspace(0, duration_in_seconds, num=samples_to_extract, endpoint=False)

# Calculate the standard deviation of the segment's amplitude
std_dev = np.std(acceleration)
max_val = np.max(data)
print(f"Standard Deviation of Acceleration: {std_dev:.4f}")
print(f"Maximum Value of Acceleration: {max_val:.4f}")

# Plot the waveform of the segment
plt.figure(figsize=(10, 4))
plt.plot(time, acceleration)
plt.title(f'10 ms Segment of Audio Waveform\nStandard Deviation: {std_dev:.4f}\nOverall max: {max_val:.4f}')
plt.xlabel('time/ s')
plt.ylabel('Acceleration ($ms^{-2}$)')
plt.grid(True)
plt.show()


# Integrate acceleration to get velocity
velocity = cumtrapz(acceleration, time, initial=0)

# Integrate velocity to get position
position = cumtrapz(velocity, time, initial=0)

# Plot acceleration, velocity, and position
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(time, acceleration, label='Acceleration')
plt.title('Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(time, velocity, label='Velocity', color='orange')
plt.title('Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(time, position, label='Position', color='green')
plt.title('Position')
plt.xlabel('Time (s)')
plt.ylabel('Position')
plt.grid(True)

plt.tight_layout()
plt.show()
