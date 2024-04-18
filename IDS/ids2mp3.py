import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.interpolate import interp1d
from scipy.signal import iirnotch, lfilter, detrend
plt.rcParams.update({'font.size': 16})


name = 'pulseTubeOFF'
#seconds
timecutoff = 20
csv_file = f"/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/IDS/IDS traces/cryostat/{name}.csv"

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
        if time > timecutoff:
            break
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
sample_rate = 50000  # Sample rate in Hz
duration = max(time_interpolated)  # Duration in seconds
t = np.linspace(0, duration, int(sample_rate * duration))
audio_signal = np.interp(t, time_interpolated, displacement_interpolated)

# Normalize audio signal
audio_signal /= np.max(np.abs(audio_signal))

# # Apply notch filter to remove frequencies around 300 Hz
# f0 = 300.0  # Frequency to be removed from the signal (Hz)
# nyquist = 0.5 * sample_rate
# w0 = f0 / nyquist
# Q = 1.0    # Quality factor
# b, a = iirnotch(w0, Q)
# audio_signal_filtered = lfilter(b, a, audio_signal)
#
# # Apply notch filter to remove frequencies around 300 Hz
# f02 = 100.0  # Frequency to be removed from the signal (Hz)
# nyquist2 = 0.5 * sample_rate
# w02 = f02 / nyquist2
# Q2 = 1.0    # Quality factor
# b2, a2 = iirnotch(w02, Q2)
# audio_signal_filtered2 = lfilter(b2, a2, audio_signal_filtered)

# Write filtered audio to file
output_file = f"{name}.wav"
write(output_file, sample_rate, audio_signal)

#calculate the variance including detrend
def detrendStdDev(displacementData):
    detrendedData = detrend(displacementData)
    variance = np.var(detrendedData)
    stddev = np.sqrt(variance)*10**9
    return detrendedData, stddev

def polyfitStdDev(time, displacementData, polyN):
    #create fit
    coeff = np.polyfit(time, displacementData, polyN)
    #remove trend
    detrendedData = displacementData - np.polyval(coeff, time)
    #stdDev
    stdDev = np.std(detrendedData)
    return detrendedData, stdDev

detrendedData, stddev = polyfitStdDev(time_data, displacement_data, 4)
stddev *= 10**9

# Plot the displacement signal
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
#plt.plot(time_data, displacement_data)
plt.plot(time_data, 10**9 * detrendedData)
plt.title(f'{name}, Std dev: {stddev:.5f}nm, 50kHz sampling')
plt.xlabel('Time (s)')
plt.xlim(0,0.01)
plt.ylabel('Amplitude/ nm')
plt.grid(True)

# Compute FFT of the filtered audio signal
n = len(displacement_data)
frequencies = np.fft.rfftfreq(n, d=1/sample_rate)
fft_values = np.abs(np.fft.rfft(displacement_data))

# Plot FFT of the filtered audio signal
plt.subplot(2, 1, 2)
plt.plot(frequencies, fft_values)
plt.xlim(0, 2000)
plt.ylim(0, max(fft_values[50:]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude/ arb')
plt.title(name)
plt.grid(True)

plt.tight_layout()
plt.savefig(f"{name}.png")  # Save figure with name variable
plt.show()

print("Filtered audio trace saved as:", output_file)
print('std dev of displacement: ', stddev)
print('baseline: ', baseline)