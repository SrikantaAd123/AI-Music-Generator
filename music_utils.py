import os
from transformers import MusicgenForConditionalGeneration, MusicgenProcessor
import torch
import torchaudio

def generate_music(prompt):
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    processor = MusicgenProcessor.from_pretrained("facebook/musicgen-small")

    inputs = processor(text=[prompt], return_tensors="pt")
    audio_values = model.generate(**inputs, max_new_tokens=1024)

    torchaudio.save("output.wav", audio_values[0], 16000)
    return "output.wav"
