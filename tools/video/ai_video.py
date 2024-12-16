import os

from moviepy.editor import VideoFileClip, AudioFileClip

# File paths
base_dir = os.path.abspath(os.path.join(os.getcwd(), "../resource"))
video_file = os.path.join(base_dir, "1.mp4")
audio_file = os.path.join(base_dir, "1.mp3")
output_file = os.path.join(base_dir, "1_output.mp4")

# Load video and audio
video = VideoFileClip(video_file)
audio = AudioFileClip(audio_file)

# Combine video with new audio
final_video = video.set_audio(audio)

# Export the final video
final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
