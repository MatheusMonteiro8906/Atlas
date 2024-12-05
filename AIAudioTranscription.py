import whisper

model = whisper.load_model("medium")
answer = model.transcribe("response.mp3")

print(answer)