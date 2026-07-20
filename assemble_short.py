from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
import os

def create_branded_short(stock_clips, audio_path, title_text, category, engagement_question, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    main_duration = audio.duration
    outro_duration = 3.0  # 3 seconds for the question card
    total_duration = main_duration + outro_duration
    
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
    label_clip = label_clip.set_position(('center', 150)).set_duration(main_duration)
    
    title_clip = TextClip(title_text, fontsize=65, color='white', font='DejaVu-Sans-Bold', 
                          method='caption', size=(900, None), align='center')
    title_clip = title_clip.set_position('center').set_duration(main_duration).fx(fadein, 0.8)
    
    brand_clip = TextClip("FitSehatzone", fontsize=45, color='#64C8FF', font='DejaVu-Sans-Bold')
    brand_clip = brand_clip.set_position(('center', 1750)).set_duration(total_duration)
    
    # Engagement question - appears only during outro, with stronger overlay for readability
    question_overlay = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_opacity(0.6)
    question_overlay = question_overlay.set_start(main_duration).set_duration(outro_duration)
    
    question_clip = TextClip(engagement_question, fontsize=55, color='#FFD700', font='DejaVu-Sans-Bold',
                             method='caption', size=(900, None), align='center')
    question_clip = question_clip.set_position('center').set_start(main_duration).set_duration(outro_duration)
    question_clip = question_clip.fx(fadein, 0.4)
    
    comment_prompt = TextClip("💬 Comment Below!", fontsize=45, color='white', font='DejaVu-Sans-Bold')
    comment_prompt = comment_prompt.set_position(('center', 1200)).set_start(main_duration).set_duration(outro_duration)
    
    layers = [background, overlay, label_clip, title_clip, brand_clip, question_overlay, question_clip, comment_prompt]
    
    if os.path.exists("logo.png"):
        logo = ImageClip("logo.png").set_duration(total_duration)
        logo = logo.resize(width=180)
        logo = logo.set_position((40, 60))
        layers.append(logo)
    
    final = CompositeVideoClip(layers)
    
    # Extend audio with silence for the outro duration
    silence = AudioClip(lambda t: 0, duration=outro_duration)
    final_audio = concatenate_audioclips([audio, silence])
    final = final.set_audio(final_audio)
    
    final.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        ffmpeg_params=['-pix_fmt', 'yuv420p']
    )
    
    return output_path
