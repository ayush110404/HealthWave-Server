import scipy.io.wavfile as wavfile
import scipy.fft as fft
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

# Function to read and preprocess the audio file
def read_audio_file(file_name):
    # Read the wav file
    fs_rate , signal = wavfile.read(file_name)
    print("Frequency sampling:", fs_rate)

    # Check the number of channels
    l_audio = len(signal.shape);
    print("Channels:", l_audio)

    # If stereo, convert to mono by averaging the two channels
    if l_audio == 2:
        signal = signal.sum(axis=1) / 2

    return fs_rate, signal

# Function to calculate time parameters
def calculate_time_params(signal, fs_rate):
    N = signal.shape[0]
    print("Complete Samplings N:", N)

    # Calculate the duration of the signal
    secs = N / float(fs_rate)
    print("secs:", secs)

    # Calculate the time step between samples
    Ts = 1.0 / fs_rate
    print("Timestep between samples Ts:", Ts)

    # Create a time vector
    t = np.arange(0, secs, Ts)

    # Ensure t and signal have the same length
    t = t[:len(signal)]
    return t, N

# Function to compute FFT
def compute_fft(signal, N, t):
    # Compute the FFT using scipy.fft
    FFT = abs(fft.fft(signal))

    # Take one side of the FFT range (positive frequencies)
    FFT_side = FFT[range(N // 2)]

    # Compute the corresponding frequencies for the FFT
    freqs = fft.fftfreq(signal.size, t[1] - t[0])

    # One side frequency range
    freqs_side = freqs[range(N // 2)]
    
    return FFT, FFT_side, freqs, freqs_side

# Function to calculate heart rate from the audio signal
def calculate_heart_rate(signal, fs_rate, time_vector):
    # Normalize the signal
    normalized_signal = (signal - np.mean(signal)) / np.std(signal)
    
    # Find peaks in the normalized signal
    peaks, _ = find_peaks(normalized_signal, height=0.5, distance=fs_rate * 0.5)
    
    # Calculate time differences between peaks
    peak_times = time_vector[peaks]
    time_diffs = np.diff(peak_times)
    
    # Calculate heart rate in beats per minute (BPM)
    heart_rates = 60 / time_diffs
    
    # Calculate average heart rate
    average_hr = np.mean(heart_rates)
    
    return average_hr, peaks

# Function to plot the results
def plot_results(t, signal, freqs, FFT, freqs_side, FFT_side, peak_indices):
    # Plot the signal, FFT, one-sided FFT, and detected peaks
    plt.figure(figsize=(12, 12))

    plt.subplot(411)
    plt.plot(t, signal, "g")  # Plotting the signal
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Original Signal')


    plt.subplot(414)
    plt.plot(t, signal, label='Signal')
    plt.plot(t[peak_indices], signal[peak_indices], "ro", label='Detected Peaks')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio Signal with Detected Heartbeats')
    plt.legend()

    plt.subplot(412)
    plt.plot(freqs, FFT, "r")  # Plotting the complete FFT spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count dbl-sided')
    plt.title('Complete FFT Spectrum')

    plt.subplot(413)
    plt.plot(freqs_side, abs(FFT_side), "b")  # Plotting the positive FFT spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')
    plt.title('One-sided FFT Spectrum')
    plt.tight_layout()
    plt.show()

def estimate_pitch(signal, fs_rate, fft_size=2048, overlap=0.5):
    hop_size = int(fft_size * (1 - overlap))
    num_frames = (len(signal) - fft_size) // hop_size + 1
    pitches = []
    
    for i in range(num_frames):
        frame = signal[i*hop_size : i*hop_size + fft_size]
        windowed_frame = frame * np.hanning(fft_size)
        spectrum = np.abs(fft.rfft(windowed_frame))
        
        # Find the index of the maximum in the spectrum
        max_index = np.argmax(spectrum)
        
        # Convert index to frequency
        pitch = max_index * fs_rate / fft_size
        pitches.append(pitch)
    
    return pitches

def process_audio_file(file_name):
    # Read and preprocess the audio file
    fs_rate, signal = read_audio_file(file_name)

    # Calculate time parameters
    t, N = calculate_time_params(signal, fs_rate)

    # Compute FFT
    # FFT, FFT_side, freqs, freqs_side = compute_fft(signal, N, t)

    # Calculate heart rate
    average_hr, peak_indices = calculate_heart_rate(signal, fs_rate, t)
    print(f"Average Heart Rate: {average_hr:.2f} BPM")

    # Estimate pitch
    pitches = estimate_pitch(signal, fs_rate)

    # Normalize pitches to range [0, 1] for easier visualization
    normalized_pitches = (pitches - np.min(pitches)) / (np.max(pitches) - np.min(pitches))

    return {
        "average_hr": average_hr,
        "peak_times": t[peak_indices].tolist(),
        "pitch_data": normalized_pitches.tolist(),
        "duration": t[-1]
    }

# Example usage
# process_audio_file("test_audio/70bpm2.wav")
# process_audio_file("upload_audio/response.wav")
