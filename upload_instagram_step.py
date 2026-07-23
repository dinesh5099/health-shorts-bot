import os
import json
from upload_instagram import upload_reel

def main():
    github_repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    public_video_url = f"https://github.com/{github_repo}/releases/download/video-{run_id}/health_short.mp4"
    
    print(f"Public video URL: {public_video_url}")
    
    # Load metadata saved by main.py
    with open('video_metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    caption = f"""{metadata['topic_title']} 🌿

{metadata['engagement_text']}

📌 Follow @fitsehatzone for daily health tips!

#FitSehatZone #HealthTips #Shorts #IndianHealth #Fitness #Wellness"""
    
    upload_reel(public_video_url, caption)

if __name__ == "__main__":
    main()
