import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime

def list_devices():
    print("Available audio devices:")
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        print(f"{index}: {device['name']} ({'input' if device['max_input_channels'] > 0 else 'output'})")

def record_audio(device_id=0, duration=20, sample_rate=44100):
    # Setting up the device
    if device_id is None:
        device_id = sd.default.device['input']
    else:
        sd.default.device = device_id

    device_info = sd.query_devices(device_id)
    device_name = device_info['name']
    print(f"Using device: {device_name}")

    # Warm-up recording (5 seconds)
    print("Warm-up recording...")
    sd.rec(int(5 * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait until warm-up recording is finished
    print("Warm-up finished.")

    # Main recording
    print("Main recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait until main recording is finished
    print("Recording finished.")

    # Generate filename with the current timestamp
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".flac"

    # Save the recorded audio
    sf.write(filename, audio, sample_rate)
    print(f"File saved as {filename}")

if __name__ == "__main__":
    list_devices()  # Optional: Uncomment to see a list of all available devices
    record_audio()  # Add the device_id argument if needed
