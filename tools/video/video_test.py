from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
import re

# Folder and file paths
image_folder = "data/image"
audio_file = "data/content_focus.mp3"
output_video = "data/final_video_test.mp4"

# Function to parse start and end times from filenames
def parse_time_from_filename(filename):
    match = re.match(r"(\d+)-(\d+)", filename)
    if match:
        start_time = int(match.group(1))
        end_time = int(match.group(2))
        return start_time - 7, end_time - 7
    return None, None

# Create image clips based on filenames with a 10-second limit
image_clips = []
cumulative_duration = 0  # Track the total duration of the video

for filename in sorted(os.listdir(image_folder)):
    filepath = os.path.join(image_folder, filename)
    
    # Parse start and end times from the filename
    start_time, end_time = parse_time_from_filename(filename)
    if start_time is not None and end_time is not None:
        duration = end_time - start_time
        # Stop adding clips once we reach 10 seconds
        if cumulative_duration + duration > 10:
            duration = 10 - cumulative_duration  # Adjust the last clip to cap at exactly 10 seconds
        
        # Create and resize the ImageClip
        clip = ImageClip(filepath).set_duration(duration).set_start(cumulative_duration)
        clip = clip.resize(1.5)  # Resize to make it larger (1.5x)
        
        image_clips.append(clip)
        
        # Update cumulative duration and stop if we reach 10 seconds
        cumulative_duration += duration
        if cumulative_duration >= 10:
            break

# Concatenate all image clips
final_video = concatenate_videoclips(image_clips, method="compose")

# Add the audio track, trimmed to 10 seconds
audio = AudioFileClip(audio_file).subclip(0, 10)
final_video = final_video.set_audio(audio)

# Export the final test video
final_video.write_videofile(output_video, codec="libx264", fps=24)

print(f"10-second test video created successfully as '{output_video}'")
