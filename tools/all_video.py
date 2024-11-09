import json
import os
import re
import datetime
import azure.cognitiveservices.speech as speechsdk
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from dotenv import load_dotenv


load_dotenv()

# Set up Azure Text-to-Speech configuration
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')        # Replace with your Azure Speech API Key
AZURE_REGION = os.getenv('AZURE_REGION')                 # Replace with your Azure Region

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"  # Example Mandarin voice

# Set the base data folder path and today's date folder
base_data_folder = "data"
today_folder_name = datetime.datetime.now().strftime("%Y%m%d")
day_folder = os.path.join(base_data_folder, today_folder_name)
input_json_path = os.path.join(day_folder, "input.json")
images_folder = os.path.join(day_folder, "images")
output_folder = os.path.join(day_folder, "output_videos")
final_video_output = os.path.join(output_folder, "final_video.mp4")

chinese_font_path = "fonts/SourceHanSerifSC-VF.otf"  # Update this to your actual font path

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load JSON data
with open(input_json_path, 'r') as f:
    data = json.load(f)

# Function to generate audio from SSML using Azure
def text_to_audio(text, audio_path):
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Generate the audio with SSML
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
        <voice name="zh-CN-YunxiNeural">
        {text}
        </voice>
    </speak>
    """
    
    result = synthesizer.speak_ssml_async(ssml_text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio content saved to '{audio_path}'")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")


# Function to clean SSML and extract text with approximate timing
def parse_ssml_to_text_segments(ssml_text, char_per_second=5):
    # Define a regex pattern to match break times
    break_pattern = re.compile(r'<break time="(\d+)ms"/>')
    
    # Split the SSML text by breaks to estimate timing for each segment
    parts = break_pattern.split(ssml_text)
    
    # Initialize variables
    text_segments = []
    current_time = 0  # Start time accumulator in milliseconds

    # Process each part to estimate duration based on text length and break time
    for i in range(0, len(parts), 2):
        # Clean out SSML tags from the text segment
        text = re.sub(r'<[^>]+>', '', parts[i]).strip()
        
        # Calculate the duration based on character count
        if text:
            text_duration = len(text) / char_per_second  # Duration in seconds
            # Include break time after this segment in the duration
            if i + 1 < len(parts):
                break_time = int(parts[i + 1]) / 1000  # Convert break time to seconds
            else:
                break_time = 0
            duration = text_duration
            text_segments.append((text, current_time / 1000, duration))  # Convert start time to seconds
            current_time += (duration * 1000)  # Convert duration back to milliseconds for cumulative time
        
        # Handle only the break time if there's no text in this part
        elif i + 1 < len(parts):
            current_time += int(parts[i + 1])  # Increment time by the break duration

    return text_segments


# Modified function to add text clips at specific times
def create_video_segment_with_text(ssml_text, image_name, index):
    audio_path = os.path.join(output_folder, f"audio_{index}.mp3")
    video_path = os.path.join(output_folder, f"video_{index}.mp4")
    
    # Generate audio from SSML
    text_to_audio(ssml_text, audio_path)
    
    # Check if the audio file was created successfully before proceeding
     # Check if the audio file was created successfully before proceeding
    if os.path.exists(audio_path):
        # Load image and set duration based on audio length
        image_path = os.path.join(images_folder, image_name)
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        image_clip = ImageClip(image_path).set_duration(duration).resize(height=720).set_audio(audio)
        
        # Parse SSML to extract text segments with approximate timings
        text_segments = parse_ssml_to_text_segments(ssml_text)

        # Create text clips based on parsed SSML timing information
        text_clips = [
            TextClip(txt, fontsize=30, color='white', font=chinese_font_path, bg_color='#42423F', 
             stroke_color='white', stroke_width=0.5)
            .set_position(("center", 640))  # Moves text slightly above the bottom of the screen
            # .margin(bottom=50)
            .set_start(start_time)           # Set the start time for each text segment
            .set_duration(duration)          # Use calculated duration to keep text visible
            for txt, start_time, duration in text_segments
        ]

        
        # Combine the image and text clips
        video_clip = CompositeVideoClip([image_clip] + text_clips)
        
        # Write the final video segment
        video_clip.write_videofile(video_path, codec="libx264", fps=24)
        return video_path
    else:
        print(f"Error: Audio file '{audio_path}' not found.")
        return None


def trim_video_end(video_path, trim_duration=0.1):
    """Trim a small portion from the end of the video to avoid overlap."""
    video = VideoFileClip(video_path)
    duration = max(0, video.duration - trim_duration)  # Trim duration from end
    trimmed_video = video.subclip(0, duration)
    return trimmed_video

# Concurrent processing for each text-image pair, preserving order
video_segment_paths = [None] * len(data)  # Initialize a list to maintain order

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(create_video_segment_with_text, item["text"], item["image"], idx): idx for idx, item in enumerate(data)}
    for future in futures:
        index = futures[future]
        video_segment_paths[index] = future.result()  # Store the video path as a result

# Load and trim each video file
video_segments = [trim_video_end(path, trim_duration=0.1) for path in video_segment_paths if path]

# Concatenate all video segments into a final video
final_video = concatenate_videoclips(video_segments, method="compose")
final_video.write_videofile(final_video_output, codec="libx264", fps=24)


print(f"Final video created at: {final_video_output}")

# Upload to YouTube (optional, if you have a YouTube API setup, you would add the upload code here)
# For example, you can use `pytube` or `googleapiclient` for this part.
