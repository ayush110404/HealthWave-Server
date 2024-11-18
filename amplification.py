import numpy as np
import librosa
import soundfile as sf
from scipy import signal

def bandpass_filter_and_amplify(data, fs, lowcut=20, highcut=50, order=6, amplification=2):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_signal = signal.filtfilt(b, a, data)
    amplified_signal = filtered_signal * amplification
    return amplified_signal

def process_audio_file(input_file, output_file, lowcut=20, highcut=50, order=6, amplification=2):
    """
    Process an audio file with a band-pass filter and amplification.
    
    Parameters:
    - input_file: path to the input audio file
    - output_file: path to save the processed audio file
    - lowcut: lower frequency of the band-pass filter (default: 20 Hz)
    - highcut: higher frequency of the band-pass filter (default: 50 Hz)
    - order: order of the filter (default: 6)
    - amplification: amplification factor (default: 2)
    """
    try:
        # Load the audio file
        y, sr = librosa.load(input_file, sr=None)
        
        print(f"Loaded audio file: duration={len(y)/sr:.2f}s, sample rate={sr}Hz")
        
        # Check for non-finite values in input
        if not np.isfinite(y).all():
            print("Warning: Input audio contains non-finite values. Replacing with zeros.")
            y = np.nan_to_num(y)
        
        # Apply the band-pass filter and amplification
        processed_audio = bandpass_filter_and_amplify(y, sr, lowcut, highcut, order, amplification)
        
        # Check for non-finite values after processing
        if not np.isfinite(processed_audio).all():
            print("Warning: Processed audio contains non-finite values. Replacing with zeros.")
            processed_audio = np.nan_to_num(processed_audio)
        
        # Normalize the processed audio to prevent clipping
        max_val = np.max(np.abs(processed_audio))
        if max_val > 0:
            processed_audio = processed_audio / max_val
        else:
            print("Warning: Processed audio is silent.")
        
        # Save the processed audio
        sf.write(output_file, processed_audio, sr)
        
        print(f"Processed audio saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Debug information:")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Filter parameters: lowcut={lowcut}, highcut={highcut}, order={order}, amplification={amplification}")

# Example usage
input_file = "upload_audio/response.wav"
output_file = "upload_audio/processed_audio.wav"
process_audio_file(input_file, output_file)