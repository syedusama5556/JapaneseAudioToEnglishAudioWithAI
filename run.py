import os
from spleeter.separator import Separator

# Define input and output directories
input_dir = "input/"
output_dir = "output/"

# Load the pre-trained AI model
separator = Separator('spleeter:2stems')

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".mp3") or filename.endswith(".wav"):
        # Load the audio file
        audio_file = os.path.join(input_dir, filename)
        print(audio_file)
        # Separate the vocals and background music
        separated_audio = separator.separate_to_file("01.mp3", output_dir, synchronous=False)

        print(f"Separation complete for {filename}")
separator.join()