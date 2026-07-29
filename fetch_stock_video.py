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

def get_stock_clips(keywords, num_clips=10):
    """Fetches unique clips across all keywords, avoiding duplicates"""
    all_urls = []
    seen_urls = set()
    
    for keyword in keywords:
        urls = search_pexels_videos(keyword, per_page=5)
        for url in urls:
            if url not in seen_urls:
                seen_urls.add(url)
                all_urls.append(url)
    
    print(f"Found {len(all_urls)} unique video URLs across {len(keywords)} keywords")
    
    clip_paths = []
    for i, url in enumerate(all_urls[:num_clips]):
        path = f"stock_clip_{i}.mp4"
        try:
            download_video(url, path)
            clip_paths.append(path)
        except Exception as e:
            print(f"Failed to download clip {i}: {e}")
    
    if len(clip_paths) < 3:
        print(f"WARNING: Only found {len(clip_paths)} unique clips")
    
    return clip_paths

if __name__ == "__main__":
    clips = get_stock_clips(["yoga", "meditation", "wellness"])
    print(f"Downloaded {len(clips)} unique clips")
