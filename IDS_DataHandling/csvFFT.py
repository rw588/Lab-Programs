import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import detrend

# Read the CSV file
filename = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/IDS/IDS traces/cryostat/840mK.csv'
filename = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/IDS/IDS traces/cryostat/pulseTubeOFF.csv'
filename = "/Users/robertwaddy/Downloads/75mKpulseOnNoTurbo.csv"

#samplingFrequency = 50000  # 50 kHz
samplingFrequency = 1000000  # 100 MHz

data = pd.read_csv(filename, delimiter=';', skiprows=4)

# Convert time to seconds and length from pm to nm
data['Time'] = data['Time'].astype(float)
data['wibblywobbly'] = data['wibblywobbly'].astype(float) / 1000  # Convert pm to nm

# Subtract the baseline
baseline = np.mean(data['wibblywobbly'])
data['wibblywobbly'] = data['wibblywobbly'] - baseline

# Plot the trace in a 0.01s window
trace_window = 0.01  # seconds
trace_data = data[data['Time'] <= trace_window]

# Detrend the trace data
trace_data_detrended = detrend(trace_data['wibblywobbly'])

# Calculate the standard deviation of the detrended trace data
std_detrended = np.std(trace_data_detrended)

# Create a figure with two subplots and increase the space between them
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.5})

# Plot the trace
ax1.plot(trace_data['Time'], trace_data_detrended)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Position [nm]')
ax1.set_title(f'Pulse tube off slowly warming from base. Detrended Position vs. Time (0.01s window)\nStandard Deviation: {std_detrended:.3f} nm. {samplingFrequency/1000:.0f} kHz sampling')
ax1.grid(True)

# Convert the 'wibblywobbly' column to a NumPy array for FFT
wibblywobbly_array = data['wibblywobbly'].to_numpy()

# FFT over the whole data set
N = len(wibblywobbly_array)
T = 1 / samplingFrequency
yf = fft(wibblywobbly_array)
xf = fftfreq(N, T)[:N // 2]

# Plot the FFT
ax2.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Amplitude [arb]')
ax2.set_xlim([0, 3000])
ax2.set_title('FFT of Position Data')
ax2.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
