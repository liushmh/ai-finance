import json
import os
from concurrent.futures import ThreadPoolExecutor
from google.cloud import texttospeech
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips
import uuid
import datetime

# Setup Google Cloud Text-to-Speech
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
tts_client = texttospeech.TextToSpeechClient()

# Set the base data folder path and today's date folder
base_data_folder = "data"
today_folder_name = datetime.datetime.now().strftime("%Y%m%d")
day_folder = os.path.join(base_data_folder, today_folder_name)
input_json_path = os.path.join(day_folder, "input.json")
images_folder = os.path.join(day_folder, "images")
output_folder = os.path.join(day_folder, "output_videos")
final_video_output = os.path.join(output_folder, "final_video.mp4")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load JSON data
with open(input_json_path, 'r') as f:
    data = json.load(f)

# Function to generate audio from SSML
def text_to_audio(text, audio_path):
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(language_code="cmn-CN", name='cmn-CN-Wavenet-C', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(audio_path, "wb") as out:
        out.write(response.audio_content)

# Function to combine image and audio into a video clip
def create_video_segment(text, image_name, index):
    audio_path = os.path.join(output_folder, f"audio_{index}.mp3")
    video_path = os.path.join(output_folder, f"video_{index}.mp4")
    
    # Generate audio from text
    text_to_audio(text, audio_path)
    
    # Load image and set duration based on audio length
    image_path = os.path.join(images_folder, image_name)
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    image_clip = ImageClip(image_path).set_duration(duration).resize(height=720).set_audio(audio)
    
    # Write video segment
    image_clip.write_videofile(video_path, codec="libx264", fps=24)
    return video_path

# Concurrent processing for each text-image pair, preserving order
video_segments = [None] * len(data)  # Initialize a list to maintain order

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(create_video_segment, item["text"], item["image"], idx): idx for idx, item in enumerate(data)}
    for future in futures:
        index = futures[future]
        video_segments[index] = future.result()  # Place result in correct order

# Combine all video segments into a final video
clips = [VideoFileClip(clip) for clip in video_segments]  # Use VideoFileClip here, not AudioFileClip
final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile(final_video_output, codec="libx264", fps=24)

print(f"Final video created at: {final_video_output}")

# Upload to YouTube (optional, if you have a YouTube API setup, you would add the upload code here)
# For example, you can use `pytube` or `googleapiclient` for this part.
