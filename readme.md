# HealthWave BPM Calculator - Backend

## 🌟 Project Overview

HealthWave BPM Calculator is an advanced heart rate monitoring solution that leverages audio signal processing to accurately calculate beats per minute (BPM) in real-time. This backend server provides a robust API for heart rate analysis using sophisticated signal processing techniques.

## 🚀 Features

- **Advanced Audio Processing**: Utilizes Fast Fourier Transform (FFT) for precise heart rate calculation
- **Multiple Audio Format Support**: Converts and processes various audio file types
- **Real-time BPM Calculation**: Quickly analyzes audio input to determine heart rate
- **Flexible API Endpoints**: Easy integration with frontend applications
- **Signal Amplification and Filtering**: Advanced audio signal enhancement techniques

## 🛠 Technologies Used

- **Backend**: Flask
- **Signal Processing**: 
  - NumPy
  - SciPy
  - Matplotlib
- **Audio Processing**: 
  - Librosa
  - PyDub
- **Language**: Python 3.8+

## 📦 Prerequisites

- Python 3.8 or higher
- pip package manager


## Installation
To install and run the BPM Calculator, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/ayush110404/HeathWave-Server.git
    ```
2. Navigate to the project directory:
    ```bash
    cd HealthWave-Server
    ```
3. Create a virtual environment (recommended):
 ```
 bash
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate
```
3. Install the required dependencies:
    ```bash
    python install numpy scipy matplotlib flask pydub
    ```
4. To start the server:
    ```bash
    python server.py
    The server will start running on `http://localhost:5000`
    ```

## 📡 API Endpoints

### `/audio` (POST)
- **Description**: Process audio file and calculate heart rate
- **Input**: Raw audio file (m4a, wav)
- **Output**: JSON with heart rate analysis

### `/about`
- **Description**: Returns basic server information


## 🔬 Signal Processing Techniques
- Fast Fourier Transform (FFT)
- Bandpass Filtering
- Peak Detection
- Pitch Estimation



## 🙏 Acknowledgements

- NumPy
- SciPy
- Flask
- Librosa
