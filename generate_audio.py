import asyncio
import edge_tts
import random

HINDI_VOICES = {
    "male": "hi-IN-MadhurNeural",
    "female": "hi-IN-SwaraNeural"
}

async def text_to_speech(text, output_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def create_audio(text, output_path="narration.mp3", voice_gender=None):
    if voice_gender is None:
        voice_gender = random.choice(["male", "female"])
    
    voice = HINDI_VOICES[voice_gender]
    asyncio.run(text_to_speech(text, output_path, voice))
    
    print(f"Audio generated using {voice_gender} voice ({voice})")
    return output_path, voice_gender

if __name__ == "__main__":
    create_audio("यह एक परीक्षण है।", "test.mp3")
