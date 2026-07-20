from fetch_topic import get_next_topic
from generate_audio import create_audio
from generate_visual import create_visual
from assemble_short import create_short

def run_pipeline():
    print("1. Selecting topic...")
    category, topic = get_next_topic()
    print(f"   Category: {category}")
    print(f"   Title: {topic['title']}")
    
    print("2. Creating visual...")
    visual_path = create_visual(topic['title'], category)
    
    print("3. Generating Hindi audio...")
    audio_path, voice_used = create_audio(topic['hindi_script'])
    print(f"   Voice: {voice_used}")
    
    print("4. Assembling short...")
    video_path = create_short(visual_path, audio_path)
    
    print(f"Done! Video: {video_path}")
    print(f"Title (for YouTube): {topic['title']}")
    return video_path

if __name__ == "__main__":
    run_pipeline()
