import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, find_peaks
import soundfile as sf
import os

def calculate_heart_rate(audio_file_path):
    try:
        # Check if file exists
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"The file {audio_file_path} does not exist.")

        # Try reading with scipy.io.wavfile
        try:
            sample_rate, audio_data = wavfile.read(audio_file_path)
        except ValueError:
            # If scipy fails, try with soundfile
            audio_data, sample_rate = sf.read(audio_file_path)

        # Print audio file information
        print(f"Successfully read audio file:")
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Duration: {len(audio_data) / sample_rate:.2f} seconds")
        print(f"Channels: {audio_data.shape[1] if len(audio_data.shape) > 1 else 1}")

        # If stereo, convert to mono
        if len(audio_data.shape) == 2:
            audio_data = np.mean(audio_data, axis=1)
        
        # Apply bandpass filter
        nyquist_freq = 0.5 * sample_rate
        low = 20 / nyquist_freq
        high = 200 / nyquist_freq
        b, a = butter(4, [low, high], btype='band')
        filtered_audio = filtfilt(b, a, audio_data)
        
        # Find peaks (potential heartbeats)
        peaks, _ = find_peaks(filtered_audio, distance=sample_rate//2)  # Adjust distance as needed
        
        # Calculate heart rate
        if len(peaks) > 1:
            avg_peak_distance = np.mean(np.diff(peaks))
            heart_rate = 60 * sample_rate / avg_peak_distance
            return heart_rate
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Usage
audio_file_path = 'bpm4.wav'
bpm = calculate_heart_rate(audio_file_path)
if bpm:
    print(f"Estimated heart rate: {bpm:.2f} BPM")
else:
    print("Could not estimate heart rate from the given audio")