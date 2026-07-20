from fetch_topic import get_next_topic
from generate_audio import create_audio
from fetch_stock_video import get_stock_clips
from assemble_short import create_branded_short
from generate_metadata import generate_title, generate_description
from upload_youtube import upload_video
from check_topic_count import check_and_alert
from send_alert import send_email
import os
import traceback

def run_pipeline():
    print("1. Selecting topic...")
    category, topic = get_next_topic()
    print(f"   Title: {topic['title']}")
    
    print("2. Fetching stock clips...")
    stock_clips = get_stock_clips(topic['keywords'], num_clips=3)
    
    print("3. Generating Hindi audio...")
    audio_path, voice_used = create_audio(topic['hindi_script'])
    
    print("4. Assembling video...")
    video_path = create_branded_short(
        stock_clips, audio_path, topic['title'], category, topic['engagement_text']
    )
    
    print("5. Generating metadata...")
    yt_title = generate_title(topic['title'])
    yt_description = generate_description(topic['title'], topic['engagement_text'], category)
    
    print("6. Uploading to YouTube...")
    video_id = upload_video(video_path, yt_title, yt_description, 
                             tags=["health", "fitness", "india", "shorts"])
    
    for clip in stock_clips:
        if os.path.exists(clip):
            os.remove(clip)
    
    print("7. Checking topic count for low-topic alert...")
    check_and_alert()
    
    print(f"Done! Video ID: {video_id}")
    return video_id

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"ERROR: {error_details}")
        
        subject = "🔴 FitSehatZone Bot: Workflow Failed"
        body = f"""Hi,

The video generation/upload pipeline failed with this error:

{str(e)}

Full traceback:
{error_details}

Please check the GitHub Actions logs for more details.

- FitSehatZone Bot"""
        send_email(subject, body)
        
        raise  # Re-raise so GitHub Actions still shows the run as failed
