from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
import re

# Folder and file paths
image_folder = "data/image"
audio_file = "data/content_focus.mp3"
output_video = "data/final_video.mp4"

# Function to parse start and end times from filenames
def parse_time_from_filename(filename):
    match = re.match(r"(\d+)-(\d+)", filename)
    if match:
        start_time = int(match.group(1))
        end_time = int(match.group(2))
        return start_time - 7, end_time - 7
    return None, None

# Create image clips based on filenames and resize
image_clips = []
for filename in sorted(os.listdir(image_folder)):
    filepath = os.path.join(image_folder, filename)
    
    # Parse start and end times from the filename
    start_time, end_time = parse_time_from_filename(filename)
    if start_time is not None and end_time is not None:
        duration = end_time - start_time
        # Create an ImageClip, resize to make it larger
        clip = ImageClip(filepath).set_duration(duration).set_start(start_time)
        
        # Resize the image to make it larger (e.g., scaling to 1.5 times the original size)
        clip = clip.resize(1.5)
        
        image_clips.append(clip)

# Concatenate all image clips
final_video = concatenate_videoclips(image_clips, method="compose")

# Add the audio track
audio = AudioFileClip(audio_file)
final_video = final_video.set_audio(audio)

# Export the final video
final_video.write_videofile(output_video, codec="libx264", fps=24)

print(f"Video created successfully as '{output_video}'")
