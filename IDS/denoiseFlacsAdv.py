import os
import numpy as np
import soundfile as sf

def detect_noise(data, threshold=0.0005, min_length=1000):
    """ Detect noisy sections as spikes above a certain threshold.
        `min_length` is roughly 0.1 seconds at 44100 Hz sampling rate. """
    noisy_indices = np.where(data > threshold)[0]
    if len(noisy_indices) == 0:
        return []
    
    # Group noisy indices into segments
    segments = []
    start = noisy_indices[0]
    for i in range(1, len(noisy_indices)):
        if noisy_indices[i] - noisy_indices[i - 1] > min_length:
            segments.append((start, noisy_indices[i - 1] + min_length))
            start = noisy_indices[i]
    segments.append((start, noisy_indices[-1] + min_length))
    return segments

def remove_noise(data, segments):
    """ Remove the noisy segments from the data """
    for start, end in segments:
        data[start:end] = 0
    return data

def process_files(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for file_name in os.listdir(source_dir):
        if file_name.endswith('.flac'):
            file_path = os.path.join(source_dir, file_name)
            data, samplerate = sf.read(file_path)
            
            # Assume the data is mono for simplicity; adjust if stereo
            if len(data.shape) > 1:
                data = data[:,0]
                
            noise_segments = detect_noise(np.abs(data))
            clean_data = remove_noise(data, noise_segments)
            
            target_file_path = os.path.join(target_dir, file_name)
            sf.write(target_file_path, clean_data, samplerate)

# Example usage
source_dir = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronData'
target_dir = '/Users/robertwaddy/Library/CloudStorage/OneDrive-Personal/PhD Experimental/Accelerometer/AccelerometerCronDataDeNoisedAdv005'
process_files(source_dir, target_dir)
