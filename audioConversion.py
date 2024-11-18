import os
from pydub import AudioSegment
import datetime

def convert_m4a_to_wav(input_file, output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    try:
        # Load the M4A file
        audio = AudioSegment.from_file(input_file, format="m4a")

        # Export as WAV
        audio.export(output_file, format="wav")

        print(f"Conversion successful. WAV file saved as '{output_file}'")
        return output_file
    except Exception as e:
        print(f"An error occurred during conversion: {str(e)}")
        return None

# Example usage
# input_file = "test_audio/75bpm.m4a"
# output_file = f"test_audio/record-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.wav"

# convert_m4a_to_wav(input_file, output_file)