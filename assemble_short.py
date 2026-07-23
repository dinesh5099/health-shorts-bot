from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from create_circular_logo import create_circular_logo_with_ring
import os

def create_branded_short(stock_clips, audio_path, title_text, category, engagement_text, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    if not stock_clips:
        raise ValueError("No stock clips provided")
    
    clip_duration = total_duration / len(stock_clips)
    
    processed_clips = []
    for clip_path in stock_clips:
        clip = VideoFileClip(clip_path)
        clip = clip.subclip(0, min(clip_duration, clip.duration))
        clip = clip.resize(height=1920)
        
        if clip.w > 1080:
            x_center = clip.w / 2
            clip = clip.crop(x_center=x_center, width=1080)
        
        clip = clip.fx(fadein, 0.3).fx(fadeout, 0.3)
        processed_clips.append(clip)
    
    background = concatenate_videoclips(processed_clips, method="compose")
    background = background.subclip(0, total_duration)
    background = background.without_audio()
    
    overlay = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_opacity(0.35).set_duration(total_duration)
    
    category_label = "HEALTH TIP" if category == "tips_and_tricks" else "NUTRITION FACT"
    label_clip = TextClip(category_label, fontsize=50, color='#64C8FF', font='DejaVu-Sans-Bold')
    label_clip = label_clip.set_position(('center', 150)).set_duration(total_duration)
    
    title_duration = total_duration * 0.65
    title_clip = TextClip(title_text, fontsize=65, color='white', font='DejaVu-Sans-Bold', 
                          method='caption', size=(900, None), align='center')
    title_clip = title_clip.set_position(('center', 700)).set_duration(title_duration).fx(fadein, 0.8).fx(fadeout, 0.5)
    
    question_start = title_duration + 0.2
    question_duration = total_duration - question_start
    question_clip = TextClip(engagement_text, fontsize=55, color='#FFD700', font='DejaVu-Sans-Bold',
                             method='caption', size=(900, None), align='center')
    question_clip = question_clip.set_position(('center', 700)).set_start(question_start).set_duration(question_duration)
    question_clip = question_clip.fx(fadein, 0.5)
    
    brand_clip = TextClip("FitSehatzone", fontsize=45, color='#64C8FF', font='DejaVu-Sans-Bold')
    brand_clip = brand_clip.set_position(('center', 1750)).set_duration(total_duration)
    
    layers = [background, overlay, label_clip, title_clip, question_clip, brand_clip]
    
    if os.path.exists("logo.png"):
        ring_color = (100, 200, 255) if category == "tips_and_tricks" else (150, 255, 150)
        circular_logo_path = create_circular_logo_with_ring(
            "logo.png", "logo_circular.png", size=160, ring_color=ring_color
        )
        logo = ImageClip(circular_logo_path).set_duration(total_duration)
        logo = logo.set_position((50, 80))
        logo = logo.fx(fadein, 0.5)
        layers.append(logo)
    
    final = CompositeVideoClip(layers)
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
