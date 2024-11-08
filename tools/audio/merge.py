import os
from pydub import AudioSegment

# Define the path to the folder containing the audio files
data_folder = 'data'

# Load each audio file from the 'data' folder
start = AudioSegment.from_mp3(os.path.join(data_folder, "start.mp3"))
content_focus = AudioSegment.from_mp3(os.path.join(data_folder, "content_focus.mp3"))
# content = AudioSegment.from_mp3(os.path.join(data_folder, "content.mp3"))
# content_main = AudioSegment.from_mp3(os.path.join(data_folder, "content_main.mp3"))
# ending = AudioSegment.from_mp3(os.path.join(data_folder, "ending.mp3"))

# Concatenate the audio files in the desired order
final_audio = start + content_focus

# Export the result as a new mp3 file in the 'data' folder
final_audio.export(os.path.join(data_folder, "20241106.mp3"), format="mp3")

print("Audio files merged successfully into 'data/20241106.mp3'")
