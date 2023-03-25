import requests
import json
import os
import base64
import whisper
from pydub import AudioSegment
from googletrans import Translator
import ffmpeg
import subprocess

#https://beta.elevenlabs.io/sign-up#google-sign-in key 736e7637027dcbad06be7f999b7c936f

ELEVENLABS_API_KEY = "736e7637027dcbad06be7f999b7c936f"



def extract_audio_from_video(video_file_path, output_dir):
    # Set the output file path
    output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(video_file_path))[0] + ".wav")
    
    # Load the video file and extract audio using ffmpeg
    try:
        stream = ffmpeg.input(video_file_path)
        audio = stream.audio
        audio = ffmpeg.output(audio, output_file_path)
        ffmpeg.run(audio, overwrite_output=True)
        return output_file_path
    except ffmpeg.Error as e:
        print(f"An error occurred while extracting audio from {video_file_path}: {e.stderr}")
        return None



video_file_path = "callofnight.mkv"
output_dir = "output"
extract_audio_from_video(video_file_path, output_dir)


# Define the paths for the input and output audio files
# input_file = str(os.getcwd())+"\jpinput\wet-anime-vocal-female.wav"
input_file = "wet-anime-vocal-female.mp3"
input_file = "output/callofnight.wav"
output_file = "../jpinput/english/audiofile"

print(input_file)
# Load the Japanese audio file and convert it to base64 encoding
# japanese_audio = AudioSegment.from_file(input_file, format="mp3")
# audio_content = base64.b64encode(japanese_audio.export(format="wav").read()).decode('utf-8')

# Instantiate a Whisper object and use it to transcribe the Japanese audio to English

model = whisper.load_model("small")
japanese_text = model.transcribe(input_file)

print("text in JP DONE")

response_dict = japanese_text

print("text in JP escaped DONE")

# Extract the "text" and "segments" fields
# text = response_dict["text"]
segments = response_dict['segments']

# Write the segments into an SRT file format
with open("output_ja.srt", "w", encoding='utf-8') as f_ja, \
     open("output_en.srt", "w", encoding='utf-8') as f_en:

    segment_index = 1
    batch_size = len(segments)  # number of segments to translate in each batch
    batch = []
    
    for segment in segments:
        start_time = segment["start"]
        end_time = segment["end"]
        segment_text = segment["text"]
        
        # Write the segment index
        f_ja.write(str(segment_index) + "\n")
        f_en.write(str(segment_index) + "\n")
        
        # Write the segment time range
        time_range = "{:.3f}".format(start_time).replace(".", ",") + " --> " + "{:.3f}".format(end_time).replace(".", ",") + "\n"
        f_ja.write(time_range)
        f_en.write(time_range)
        
        translator = Translator()
        translation_en = translator.translate(segment_text, dest="en").text

        f_ja.write(f"{segment_text}\n\n")
        
        # Write the translated segment to the English file
        f_en.write(f"{translation_en}\n\n")

        
        segment_index += 1

# all text translation
translator = Translator()

english_text = translator.translate(japanese_text['text'], dest="en").text

print("JP text in EN SRT DONE")


# Synthesize the English text using the Whisper object
headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': ELEVENLABS_API_KEY,
    'Content-Type': 'application/json',
}

json_data = {
    'text': english_text,
}

# response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM', headers=headers, json=json_data)

# with open('audio_en_response.mp3', 'wb') as f:
#     f.write(response.content)
