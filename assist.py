import os
import time
import io
import tempfile
from openai import OpenAI
from pygame import mixer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client and mixer
client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"}, api_key=os.getenv('API_KEY'))
mixer.init()

# Retrieve assistant and thread once (avoids repetitive retrieval)
assistant = client.beta.assistants.retrieve(os.getenv('ASSISTANT_ID'))
thread = client.beta.threads.retrieve(os.getenv('THREAD_ID'))

def ask_question_memory(question):
    global thread
    # Create a new message in the thread
    client.beta.threads.messages.create(thread.id, role="user", content=question)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

    # Polling for the run status with a reduced sleep time
    while (run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
        if run_status.status == 'failed':
            return "The run failed."
        time.sleep(0.1)  # Reduced sleep time for faster polling
    
    # Retrieve the response message
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def generate_tts(sentence):
    # Stream TTS output to a temporary file
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    
    # Create a temporary file to store the audio
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        response.stream_to_file(temp_file_path)
        
        # Read the file into BytesIO
        audio_buffer = io.BytesIO()
        with open(temp_file_path, 'rb') as f:
            audio_buffer.write(f.read())
        audio_buffer.seek(0)
    
    return audio_buffer

def play_sound(audio_buffer):
    # Pygame mixer doesn't accept BytesIO directly, so we use the temporary file
    mixer.music.load(audio_buffer, "mp3")
    mixer.music.play()

def TTS(text):
    audio_buffer = generate_tts(text)
    play_sound(audio_buffer)
    
    while mixer.music.get_busy():
        time.sleep(0.1)  # Reduced check time for faster response
    mixer.music.unload()  # Clean up the music after playing
    return "done"

# Example usage:
# question = "make it slightly vary every time"
# response = ask_question_memory(question)
# print(response)
