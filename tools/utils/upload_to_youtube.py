from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from collections import Counter
import string
import datetime


def upload_to_youtube(video_path, text_data):

    today_date = datetime.datetime.now().strftime("%Y%m%d")

    """Upload the final video to YouTube."""
    # Concatenate all text from the data
    combined_text = " ".join([item['text'] for item in text_data])
    
    # Extract Chinese keywords for the description

    # Generate video title
    title = f"ai云财经 {today_date}"

    # Load credentials (ensure `token.json` exists with valid YouTube API credentials)
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.upload'])
    youtube = build('youtube', 'v3', credentials=creds)

    # Prepare the request body
    request_body = {
        "snippet": {
            "title": title,
            "description": "",
            "tags": ["AI", "财经", "视频", "分析", "云科技", "新闻"],  # Add Chinese tags
            "categoryId": "25"  # Category ID for "News & Politics"
        },
        "status": {
            "privacyStatus": "public"  # Options: "public", "unlisted", "private"
        }
    }

    # Media file upload
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    # Upload the video
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print(f"Video uploaded to YouTube. Video ID: {response['id']}")
