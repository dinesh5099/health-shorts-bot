import os
from upload_instagram import upload_reel

def main():
    github_repo = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    public_video_url = f"https://github.com/{github_repo}/releases/download/video-{run_id}/health_short.mp4"
    
    print(f"Public video URL: {public_video_url}")
    
    caption = "Daily Health Tip 🌿 #FitSehatZone #HealthTips #Shorts"
    
    upload_reel(public_video_url, caption)

if __name__ == "__main__":
    main()
