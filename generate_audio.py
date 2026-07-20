import asyncio
import edge_tts
import random
from pydub import AudioSegment
from pydub.silence import split_on_silence

HINDI_VOICES = {
    "male": "hi-IN-MadhurNeural",
    "female": "hi-IN-SwaraNeural"
}

async def text_to_speech(text, output_path, voice):
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    await communicate.save(output_path)

def trim_silence_gaps(input_path, output_path, silence_thresh=-40, min_silence_len=400, keep_silence=150):
    audio = AudioSegment.from_mp3(input_path)
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    combined = AudioSegment.empty()
    for chunk in chunks:
        combined += chunk
    combined.export(output_path, format="mp3")
    return output_path

def create_audio(text, output_path="narration.mp3", voice_gender=None):
    if voice_gender is None:
        voice_gender = random.choice(["male", "female"])
    
    voice = HINDI_VOICES[voice_gender]
    raw_path = "narration_raw.mp3"
    asyncio.run(text_to_speech(text, raw_path, voice))
    
    trim_silence_gaps(raw_path, output_path)
    
    print(f"Audio generated using {voice_gender} voice ({voice}), gaps trimmed")
    return output_path, voice_gender
