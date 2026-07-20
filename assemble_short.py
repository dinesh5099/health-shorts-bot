from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

def create_branded_short(stock_clips, audio_path, title_text, category, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    if not stock_clips:
        raise ValueError("No stock clips provided")
    
    # Calculate duration per clip to fill total audio length
    clip_duration = total_duration / len(stock_clips)
    
    processed_clips = []
    for clip_path in stock_clips:
        clip = VideoFileClip(clip_path)
        clip = clip.subclip(0, min(clip_duration, clip.duration))
        clip = clip.resize(height=1920)
        
        # Center crop to 1080 width if wider
        if clip.w > 1080:
            x_center = clip.w / 2
            clip = clip.crop(x_center=x_center, width=1080)
        
        clip = clip.fx(fadein, 0.3).fx(fadeout, 0.3)
        processed_clips.append(clip)
    
    # Stitch clips together
    background = concatenate_videoclips(processed_clips, method="compose")
    background = background.subclip(0, total_duration)  # Trim to exact audio length
    background = background.without_audio()
    
    # Semi-transparent dark overlay for text readability
    overlay = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_opacity(0.35).set_duration(total_duration)
    
    # Category label
    category_label = "HEALTH TIP" if category == "tips_and_tricks" else "NUTRITION FACT"
    label_clip = TextClip(category_label, fontsize=50, color='#64C8FF', font='DejaVu-Sans-Bold')
    label_clip = label_clip.set_position(('center', 150)).set_duration(total_duration)
    
    # Main title text with fade-in
    title_clip = TextClip(title_text, fontsize=65, color='white', font='DejaVu-Sans-Bold', 
                          method='caption', size=(900, None), align='center')
    title_clip = title_clip.set_position('center').set_duration(total_duration).fx(fadein, 0.8)
    
    # Brand watermark (persistent, bottom)
    brand_clip = TextClip("FitSehatzone", fontsize=45, color='#64C8FF', font='DejaVu-Sans-Bold')
    brand_clip = brand_clip.set_position(('center', 1750)).set_duration(total_duration)
    
    # Composite everything
    final = CompositeVideoClip([background, overlay, label_clip, title_clip, brand_clip])
    final = final.set_audio(audio)
    
    final.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        ffmpeg_params=['-pix_fmt', 'yuv420p']
    )
    
    return output_path
