import sounddevice as sd 
import numpy as np
import wave 
import string

from faster_whisper import WhisperModel 
from text_parser import parse_cmd
from executor import execute_cmd

DURATION = 5
SAMPLE_RATE = 16000
INPUT_DEVICE = 7
AUDIO_FILE = "command.wave"

print("Recording for 5 secs.")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=7,
)

sd.wait()

print("Recording finished")
print(f"Peak volume: {np.max(np.abs(audio)):3f}")
print(f"Avg. volume: {np.mean(np.abs(audio)):3f}")

audio_int16 = np.int16(audio * 32767)

with wave.open(AUDIO_FILE, "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)
    wav.writeframes(audio_int16.tobytes())

print("Transcribing!")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(AUDIO_FILE)

text = " ".join(segment.text for segment in segments).strip()
text = text.translate(str.maketrans("","",string.punctuation))

# Replaces any mistakes made by the parser
text = text.replace("power off", "poweroff")
text = text.replace("shut down", "poweroff")

print(f"You said: {text}")

# Actual parsing step
command = parse_cmd(text)

if command is None:
    print("I dont understand jackshit speak better mate")
else:
    print(f"Parsed cmd: {command}")
    execute_cmd(command)
