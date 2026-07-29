from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from create_circular_logo import create_circular_logo_with_ring
import os
import random
import re

def strip_emojis_keep_punctuation(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002700-\U000027BF"
        "\U0001F900-\U0001F9FF"
        "\U00002600-\U000026FF"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub('', text).strip()

def zoom_effect(clip, zoom_ratio=0.05):
    def resize_func(t):
        return 1 + (zoom_ratio * t)
    return clip.resize(resize_func)

CATEGORY_LABELS = {
    "tips_and_tricks": "HEALTH TIP",
    "nutrition_facts": "NUTRITION FACT",
    "myth_vs_fact": "MYTH VS FACT",
    "home_remedies": "HOME REMEDY",
    "quick_facts": "DID YOU KNOW",
    "skin_hair_care": "SKIN & HAIR CARE"
}

CATEGORY_RING_COLORS = {
    "tips_and_tricks": (100, 200, 255),
    "nutrition_facts": (150, 255, 150),
    "myth_vs_fact": (255, 150, 100),
    "home_remedies": (200, 255, 100),
    "quick_facts": (255, 220, 100),
    "skin_hair_care": (255, 150, 220)
}

def create_branded_short(stock_clips, audio_path, title_text, category, engagement_text, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    if not stock_clips:
        raise ValueError("No stock clips provided")
    
    clip_duration = min(total_duration / max(len(stock_clips), 1), 2.0)
    num_clips_needed = int(total_duration / clip_duration) + 1
    
    # Build sequence avoiding immediate repeats of the same clip
    available = list(range(len(stock_clips)))
    random.shuffle(available)
    clip_sequence = []
    last_used = -1
    for i in range(num_clips_needed):
        if not available:
            available = list(range(len(stock_clips)))
            random.shuffle(available)
            # Avoid picking same as last_used if possible
            if len(available) > 1 and available[0] == last_used:
                available[0], available[1] = available[1], available[0]
        pick = available.pop()
        clip_sequence.append(pick)
        last_used = pick
    
    processed_clips = []
    for idx in clip_sequence:
        clip_path = stock_clips[idx]
        clip = VideoFileClip(clip_path)
        clip = clip.subclip(0, min(clip_duration, clip.duration))
        clip = clip.resize(height=1920)
        
        if clip.w > 1080:
            x_center = clip.w / 2
            clip = clip.crop(x_center=x_center, width=1080)
        
        clip = zoom_effect(clip, zoom_ratio=0.05)
        clip = clip.fx(fadein, 0.15).fx(fadeout, 0.15)
        processed_clips.append(clip)
    
    background = concatenate_videoclips(processed_clips, method="compose")
    background = background.subclip(0, total_duration)
    background = background.without_audio()
    
    overlay = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_opacity(0.3).set_duration(total_duration)
    
    category_label = CATEGORY_LABELS.get(category, "HEALTH TIP")
    label_clip = TextClip(category_label, fontsize=50, color='#64C8FF', font='DejaVu-Sans-Bold')
    label_clip = label_clip.set_position(('center', 150)).set_duration(total_duration)
    
    # Clean title - ensure question mark preserved, strip only emojis
    clean_title = strip_emojis_keep_punctuation(title_text)
    
    title_duration = total_duration * 0.6
    title_clip = TextClip(clean_title, fontsize=68, color='white', font='DejaVu-Sans-Bold',
                          method='caption', size=(950, None), align='center', stroke_color='black', stroke_width=2)
    title_clip = title_clip.set_position(('center', 650)).set_duration(title_duration)
    
    def title_scale(t):
        if t < 0.3:
            return 1.15 - (0.15 * (t / 0.3))
        return 1.0
    title_clip = title_clip.resize(title_scale)
    
    # Clean question text - strip emojis, guarantee "?" present
    clean_question_text = strip_emojis_keep_punctuation(engagement_text)
    if not clean_question_text.endswith('?'):
        clean_question_text += '?'
    
    question_start = title_duration + 0.15
    question_duration = total_duration - question_start
    question_clip = TextClip(clean_question_text, fontsize=58, color='#FFD700', font='DejaVu-Sans-Bold',
                             method='caption', size=(950, None), align='center', stroke_color='black', stroke_width=2)
    
    def question_position(t):
        start_y = 850
        end_y = 650
        progress = min(t / 0.4, 1.0)
        current_y = start_y - (progress * (start_y - end_y))
        return ('center', current_y)
    
    question_clip = question_clip.set_start(question_start).set_duration(question_duration)
    question_clip = question_clip.set_position(question_position)
    
    # Bold animated question mark accent graphic
    question_mark_accent = TextClip("❓", fontsize=100, color='#FFD700', font='DejaVu-Sans-Bold')
    question_mark_accent = question_mark_accent.set_position((880, 500))
    question_mark_accent = question_mark_accent.set_start(question_start).set_duration(question_duration)
    
    def qmark_scale(t):
        if t < 0.3:
            return 1.3 - (0.3 * (t / 0.3))
        return 1.0
    question_mark_accent = question_mark_accent.resize(qmark_scale)
    
    brand_clip = TextClip("FitSehatzone", fontsize=45, color='#64C8FF', font='DejaVu-Sans-Bold')
    brand_clip = brand_clip.set_position(('center', 1750)).set_duration(total_duration)
    
    emoji_accent = TextClip("✨", fontsize=80, color='white')
    emoji_accent = emoji_accent.set_position((850, 550)).set_duration(min(2.0, title_duration))
    emoji_accent = emoji_accent.fx(fadein, 0.2)
    
    layers = [background, overlay, label_clip, title_clip, question_clip, question_mark_accent, brand_clip, emoji_accent]
    
    if os.path.exists("logo.png"):
        ring_color = CATEGORY_RING_COLORS.get(category, (100, 200, 255))
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
