import json
import os
import re
import datetime
import requests
import boto3
from boto3.dynamodb.conditions import Key
import azure.cognitiveservices.speech as speechsdk
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    CompositeVideoClip
)
from dotenv import load_dotenv
from collections import defaultdict

from utils.upload_to_youtube import upload_to_youtube


load_dotenv()

# ===================== CONFIGURATION ===================== #

AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_REGION = os.getenv('AZURE_REGION')

AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"  # Example Mandarin voice

base_data_folder = "data"
today_date = datetime.datetime.now().strftime("%Y%m%d")
day_folder = os.path.join(base_data_folder, today_date)

images_folder = os.path.join(day_folder, "images")
audio_folder = os.path.join(day_folder, "audio")
video_folder = os.path.join(day_folder, "video")
final_folder = os.path.join(day_folder, "final")

final_video_output = os.path.join(final_folder, "final_video.mp4")

chinese_font_path = "fonts/SourceHanSerifSC-VF.otf"  # Update this to your actual font path

# Ensure all folders exist
for folder in [images_folder, audio_folder, video_folder, final_folder]:
    os.makedirs(folder, exist_ok=True)

# Initialize AWS S3 Client
s3_client = boto3.client('s3', region_name=AWS_REGION)

# ===================== DYNAMODB FETCH ===================== #

def fetch_news_by_date(table_name, date=None):
    """
    Fetch news data from DynamoDB by date. Defaults to today's date if no date is provided.

    Args:
        table_name (str): The name of the DynamoDB table.
        date (str): Optional. The date to fetch data for (format: YYYY-MM-DD). Defaults to today's date.

    Returns:
        list: List of news items for the specified date or today's date.
    """
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table(table_name)

    # Default to today's date if no date is provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Query for the specified date
        response = table.query(
            KeyConditionExpression=Key('date').eq(date)
        )
        items = response.get('Items', [])
        if items:
            return items[0].get('news', [])  # Return the 'news' array for the given date
        return []  # No data for the specified date
    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        return []

# ===================== FILE OPERATIONS ===================== #

def upload_to_s3(file_path, s3_key):
    try:
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, s3_key)
        print(f"Uploaded {file_path} to s3://{AWS_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")

def fetch_image_from_url(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to fetch image from {url}")

# ===================== AZURE TEXT-TO-SPEECH ===================== #

def text_to_audio(text, audio_path):
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

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
            print(f"Error details: {result.cancellation_details.error_details}")

# ===================== VIDEO GENERATION ===================== #

def parse_ssml_to_text_segments(ssml_text, char_per_second=5):
    break_pattern = re.compile(r'<break time="(\d+)ms"/>')
    parts = break_pattern.split(ssml_text)

    text_segments = []
    current_time = 0
    for i in range(0, len(parts), 2):
        text = re.sub(r'<[^>]+>', '', parts[i]).strip()
        if text:
            text_duration = len(text) / char_per_second
            break_time = int(parts[i + 1]) / 1000 if i + 1 < len(parts) else 0
            text_segments.append((text, current_time / 1000, text_duration))
            current_time += (text_duration * 1000)
        elif i + 1 < len(parts):
            current_time += int(parts[i + 1])
    return text_segments

def create_video_segment_with_text(item, index):
    text = item['text']
    image_url = item['image_url']

    # Fetch and save image
    image_path = os.path.join(images_folder, f"image_{index}.jpg")
    fetch_image_from_url(image_url, image_path)

    audio_path = os.path.join(audio_folder, f"audio_{index}.mp3")
    video_path = os.path.join(video_folder, f"video_{index}.mp4")

    # Generate audio
    text_to_audio(text, audio_path)

    # Generate video if audio exists
    if os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(audio.duration).resize(height=720).set_audio(audio)

        # Parse SSML to extract text segments
        text_segments = parse_ssml_to_text_segments(text)
        text_clips = [
            TextClip(txt, fontsize=30, color='white', font=chinese_font_path, bg_color='#42423F')
            .set_position(("center", 640))
            .set_start(start_time)
            .set_duration(duration)
            for txt, start_time, duration in text_segments
        ]

        # Combine video and text
        video_clip = CompositeVideoClip([image_clip] + text_clips)
        video_clip.write_videofile(video_path, codec="libx264", fps=24)
        return video_path
    else:
        print(f"Audio file not created: {audio_path}")
        return None


def group_video_paths_by_asset(data, video_segment_paths):
    """
    Groups video segment paths by asset.

    Args:
        data (list): List of news items.
        video_segment_paths (list): List of paths for generated video segments.

    Returns:
        dict: Dictionary where keys are assets and values are lists of video segment paths for each asset.
    """
    grouped_paths = defaultdict(list)
    for item, video_path in zip(data, video_segment_paths):
        asset = item.get("asset", "unknown")
        grouped_paths[asset].append(video_path)
    return grouped_paths

def concatenate_videos_by_asset(grouped_paths):
    """
    Concatenates video segments for each asset into a single video.

    Args:
        grouped_paths (dict): Dictionary with assets as keys and lists of video paths as values.

    Returns:
        list: List of paths to the concatenated videos for each asset.
    """
    asset_videos = []
    for asset, paths in grouped_paths.items():
        if len(paths) > 1:
            # Concatenate videos for this asset
            concatenated_path = os.path.join(final_folder, f"{asset}_combined.mp4")
            clips = [VideoFileClip(path) for path in paths]
            concatenated_video = concatenate_videoclips(clips, method="compose")
            concatenated_video.write_videofile(concatenated_path, codec="libx264", fps=24)
            asset_videos.append(concatenated_path)
        else:
            # If only one video for the asset, use it directly
            asset_videos.append(paths[0])
    return asset_videos

def concatenate_final_video(asset_videos):
    """
    Concatenates all asset videos into the final video.

    Args:
        asset_videos (list): List of paths to asset-specific concatenated videos.

    Returns:
        str: Path to the final concatenated video.
    """
    final_video_path = os.path.join(final_folder, "final_video.mp4")
    clips = [VideoFileClip(path) for path in asset_videos]
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(final_video_path, codec="libx264", fps=24)
    return final_video_path


# ===================== MAIN WORKFLOW ===================== #

def main():
    # Fetch data from DynamoDB
    data = fetch_news_by_date("YourTableName")

    video_segment_paths = [None] * len(data)  # Maintain order of video segments

    # Process video segments concurrently
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(create_video_segment_with_text, item["text"], item.get("thumbnail", ""), idx): idx
            for idx, item in enumerate(data)
        }
        for future in futures:
            index = futures[future]
            video_segment_paths[index] = future.result()

    # Group video paths by asset
    grouped_paths = group_video_paths_by_asset(data, video_segment_paths)

    # Concatenate videos by asset
    asset_videos = concatenate_videos_by_asset(grouped_paths)

    # Concatenate all asset videos into the final video
    final_video_path = concatenate_final_video(asset_videos)

    # Upload final video to S3
    upload_to_s3(final_video_path, f"final_videos/{today_date}/final_video.mp4")

    # Upload final video to YouTube
    upload_to_youtube(final_video_path, data)


if __name__ == "__main__":
    main()
