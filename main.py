from fetch_topic import get_next_topic
from generate_audio import create_audio
from fetch_stock_video import get_stock_clips
from assemble_short import create_branded_short
import os

def run_pipeline():
    print("1. Selecting topic...")
    category, topic = get_next_topic()
    print(f"   Category: {category}")
    print(f"   Title: {topic['title']}")
    
    print("2. Fetching stock video clips...")
    stock_clips = get_stock_clips(category, num_clips=3)
    print(f"   Downloaded {len(stock_clips)} clips")
    
    print("3. Generating Hindi audio...")
    audio_path, voice_used = create_audio(topic['hindi_script'])
    print(f"   Voice: {voice_used}")
    
    print("4. Assembling branded short...")
    video_path = create_branded_short(stock_clips, audio_path, topic['title'], category)
    
    # Cleanup downloaded stock clips
    for clip in stock_clips:
        if os.path.exists(clip):
            os.remove(clip)
    
    print(f"Done! Video: {video_path}")
    return video_path

if __name__ == "__main__":
    run_pipeline()
