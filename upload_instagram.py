import requests
import os
import time

INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")

def create_media_container(video_url, caption):
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media"
    
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    response = requests.post(url, params=params)
    data = response.json()
    
    if "id" not in data:
        raise Exception(f"Failed to create media container: {data}")
    
    return data["id"]

def check_container_status(container_id):
    url = f"https://graph.facebook.com/v21.0/{container_id}"
    params = {
        "fields": "status_code",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    response = requests.get(url, params=params)
    return response.json().get("status_code")

def publish_media(container_id):
    url = f"https://graph.facebook.com/v21.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    response = requests.post(url, params=params)
    return response.json()

def upload_reel(video_url, caption):
    print("Creating media container...")
    container_id = create_media_container(video_url, caption)
    print(f"Container ID: {container_id}")
    
    print("Waiting for video processing...")
    max_attempts = 30
    for attempt in range(max_attempts):
        status = check_container_status(container_id)
        print(f"Status: {status}")
        
        if status == "FINISHED":
            break
        elif status == "ERROR":
            raise Exception("Video processing failed on Instagram's side")
        
        time.sleep(10)
    else:
        raise Exception("Timed out waiting for video processing")
    
    print("Publishing...")
    result = publish_media(container_id)
    print(f"Published! Result: {result}")
    return result

if __name__ == "__main__":
    test_url = "https://example.com/test-video.mp4"
    upload_reel(test_url, "Test caption #FitSehatZone")
