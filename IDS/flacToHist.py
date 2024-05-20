import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

# Load your FLAC file
data, samplerate = sf.read("/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronData/2024-05-07_01-00-27.flac")

# Flatten the data to 1D if it's stereo (multi-channel)
if len(data.shape) > 1:
    data = data.flatten()

# Plot histogram of the sample values
plt.figure(figsize=(10, 6))
plt.hist(data, bins=100, color='blue', alpha=0.7, log=True)
plt.title('Histogram of Audio Sample Values')
plt.xlabel('Sample Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
