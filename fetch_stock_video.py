import requests
import os

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

CATEGORY_KEYWORDS = {
    "tips_and_tricks": ["yoga", "meditation", "wellness", "stretching"],
    "nutrition_facts": ["healthy food", "fruits vegetables", "cooking healthy", "diet food"]
}

def search_pexels_videos(query, per_page=3):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "portrait"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    video_urls = []
    for video in data.get("videos", []):
        # Get a reasonably sized file (not 4K, to save space/time)
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

def get_stock_clips(category, num_clips=3):
    keywords = CATEGORY_KEYWORDS.get(category, ["health"])
    clip_paths = []
    
    for i in range(num_clips):
        keyword = keywords[i % len(keywords)]
        urls = search_pexels_videos(keyword, per_page=2)
        
        if urls:
            path = f"stock_clip_{i}.mp4"
            download_video(urls[0], path)
            clip_paths.append(path)
    
    return clip_paths

if __name__ == "__main__":
    clips = get_stock_clips("tips_and_tricks")
    print(f"Downloaded {len(clips)} clips: {clips}")
