from fetch_topic import get_next_topic
from generate_audio import create_audio
from fetch_stock_video import get_stock_clips
from assemble_short import create_branded_short
import os

def run_pipeline():
    print("1. Selecting topic...")
    category, topic = get_next_topic()
    print(f"   Title: {topic['title']}")
    
    print("2. Fetching topic-specific stock clips...")
    stock_clips = get_stock_clips(topic['keywords'], num_clips=3)
    
    print("3. Generating Hindi audio (with question included)...")
    audio_path, voice_used = create_audio(topic['hindi_script'])
    
    print("4. Assembling video...")
    video_path = create_branded_short(
        stock_clips, audio_path, topic['title'], category, topic['engagement_text']
    )
    
    for clip in stock_clips:
        if os.path.exists(clip):
            os.remove(clip)
    
    print(f"Done! Video: {video_path}")
    return video_path

if __name__ == "__main__":
    run_pipeline()
