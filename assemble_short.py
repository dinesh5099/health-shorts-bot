from moviepy.editor import *

def create_short(image_path, audio_path, output_path="health_short.mp4"):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    image_clip = ImageClip(image_path).set_duration(duration)
    image_clip = image_clip.resize(newsize=(1080, 1920))
    
    final = image_clip.set_audio(audio)
    final.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        ffmpeg_params=['-pix_fmt', 'yuv420p']
    )
    return output_path
