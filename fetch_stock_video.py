import requests
import os

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def search_pexels_videos(query, per_page=5):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "portrait"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    video_urls = []
    for video in data.get("videos", []):
        for file in video["video_files"]:
            if file["width"] <= 1080:
                video_urls.append(file["link"])
                break
    return video_urls

def download_video(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path

def get_stock_clips(keywords, num_clips=5):
    """Increased default clips for faster-paced editing"""
    clip_paths = []
    
    for i in range(num_clips):
        keyword = keywords[i % len(keywords)]
        urls = search_pexels_videos(keyword, per_page=3)
        
        if urls:
            path = f"stock_clip_{i}.mp4"
            download_video(urls[0], path)
            clip_paths.append(path)
    
    return clip_paths

if __name__ == "__main__":
    clips = get_stock_clips(["yoga", "meditation"])
    print(f"Downloaded {len(clips)} clips")
