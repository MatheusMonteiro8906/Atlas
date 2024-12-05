from RealtimeSTT import AudioToTextRecorder
import assist
import time
import tools
from openai import OpenAI
import os


if __name__ == '__main__':
    client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key=os.getenv('API_KEY'))
    audio_path = os.getenv('audio_path')

    try:
        # Open the audio file
        print(audio_path)
        with open(audio_path, "rb") as audio_file:
            
            # Transcribe the audio file
            # expensive, but extremely precise
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language="pt"
            )
        # Print the transcript
        
        print(transcript)
        
    except Exception as e:
        print("An error occurred:", e)