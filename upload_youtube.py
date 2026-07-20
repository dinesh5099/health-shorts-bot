from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def get_authenticated_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, title, description, tags=None, category_id="26"):
    youtube = get_authenticated_service()
    
    body = {
        "snippet": {
            "title": title[:100],  # YouTube title limit
            "description": description[:5000],
            "tags": tags or [],
            "categoryId": category_id  # 26 = Howto & Style, good for health/fitness
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    
    video_id = response.get("id")
    print(f"Upload complete! Video ID: {video_id}")
    print(f"URL: https://youtube.com/shorts/{video_id}")
    return video_id

if __name__ == "__main__":
    upload_video("health_short.mp4", "Test Upload", "Test description", ["health", "fitness"])
