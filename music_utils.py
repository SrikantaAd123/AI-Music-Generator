import os
import torch
import torchaudio
from transformers import MusicgenForConditionalGeneration, MusicgenProcessor

def generate_music(prompt: str, output_path="output.wav"):
    # Load model and processor (this can take time)
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    processor = MusicgenProcessor.from_pretrained("facebook/musicgen-small")

    # Convert the text prompt to input tokens
    inputs = processor(text=[prompt], return_tensors="pt")

    # Generate audio tokens
    audio_values = model.generate(**inputs, max_new_tokens=1024)

    # Save generated audio
    torchaudio.save(output_path, audio_values[0], 16000)
    return output_path
