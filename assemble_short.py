from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from create_circular_logo import create_circular_logo_with_ring
import os
import numpy as np

def zoom_effect(clip, zoom_ratio=0.04):
    """Continuous slow zoom-in effect (Ken Burns style)"""
    def resize_func(t):
        return 1 + (zoom_ratio * t)
    
    return clip.resize(resize_func)

def create_branded_short(stock_clips, audio_path, title_text, category, engagement_text, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    if not stock_clips:
        raise ValueError("No stock clips provided")
    
    # Faster cuts: cap each clip at max 2 seconds
    clip_duration = min(total_duration / len(stock_clips), 2.0)
    num_clips_needed = int(total_duration / clip_duration) + 1
    
    processed_clips = []
    for i in range(num_clips_needed):
        clip_path = stock_clips[i % len(stock_clips)]
        clip = VideoFileClip(clip_path)
        
        clip = clip.subclip(0, min(clip_duration, clip.duration))
        clip = clip.resize(height=1920)
        
        if clip.w > 1080:
            x_center = clip.w / 2
            clip = clip.crop(x_center=x_center, width=1080)
        
        # Apply zoom effect for dynamic movement
        clip = zoom_effect(clip, zoom_ratio=0.05)
        
        # Quick cut transitions (very short fade, feels snappy not slow)
        clip = clip.fx(fadein, 0.15).fx(fadeout, 0.15)
        processed_clips.append(clip)
    
    background = concatenate_videoclips(processed_clips, method="compose")
    background = background.subclip(0, total_duration)
    background = background.without_audio()
    
    overlay = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_opacity(0.3).set_duration(total_duration)
    
    category_label = "HEALTH TIP" if category == "tips_and_tricks" else "NUTRITION FACT"
    category_emoji = "💪" if category == "tips_and_tricks" else "🥗"
    
    label_clip = TextClip(f"{category_emoji} {category_label}", fontsize=50, color='#64C8FF', font='DejaVu-Sans-Bold')
    label_clip = label_clip.set_position(('center', 150)).set_duration(total_duration)
    # Quick pop-in for label
    label_clip = label_clip.resize(lambda t: 1 + 0.1 * max(0, 1 - t*4) if t < 0.25 else 1)
    
    # IMMEDIATE HOOK - appears instantly at 0.0s, no fade delay, with scale-pop animation
    title_duration = total_duration * 0.6
    title_clip = TextClip(title_text, fontsize=68, color='white', font='DejaVu-Sans-Bold', 
                          method='caption', size=(950, None), align='center', stroke_color='black', stroke_width=2)
    title_clip = title_clip.set_position(('center', 650)).set_duration(title_duration)
    
    # Pop-in scale animation (starts slightly bigger, settles to normal size) - feels punchy
    def title_scale(t):
        if t < 0.3:
            return 1.15 - (0.15 * (t / 0.3))
        return 1.0
    title_clip = title_clip.resize(title_scale)
    
    # Engagement question with slide-up animation
    question_start = title_duration + 0.15
    question_duration = total_duration - question_start
    question_clip = TextClip(engagement_text, fontsize=58, color='#FFD700', font='DejaVu-Sans-Bold',
                             method='caption', size=(950, None), align='center', stroke_color='black', stroke_width=2)
    
    def question_position(t):
        # Slides up from below into position
        start_y = 850
        end_y = 650
        progress = min(t / 0.4, 1.0)
        current_y = start_y - (progress * (start_y - end_y))
        return ('center', current_y)
    
    question_clip = question_clip.set_start(question_start).set_duration(question_duration)
    question_clip = question_clip.set_position(question_position)
    
    brand_clip = TextClip("FitSehatzone", fontsize=45, color='#64C8FF', font='DejaVu-Sans-Bold')
    brand_clip = brand_clip.set_position(('center', 1750)).set_duration(total_duration)
    
    # Emoji accent overlays - subtle bounce, appears with title
    emoji_accent = TextClip("✨", fontsize=80, color='white')
    emoji_accent = emoji_accent.set_position((850, 550)).set_duration(min(2.0, title_duration))
    emoji_accent = emoji_accent.fx(fadein, 0.2)
    
    layers = [background, overlay, label_clip, title_clip, question_clip, brand_clip, emoji_accent]
    
    if os.path.exists("logo.png"):
        ring_color = (100, 200, 255) if category == "tips_and_tricks" else (150, 255, 150)
        circular_logo_path = create_circular_logo_with_ring(
            "logo.png", "logo_circular.png", size=160, ring_color=ring_color
        )
        logo = ImageClip(circular_logo_path).set_duration(total_duration)
        logo = logo.set_position((50, 80))
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
