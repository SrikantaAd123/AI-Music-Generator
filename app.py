import streamlit as st
import numpy as np
from midiutil import MIDIFile
import tempfile
import time
import os

st.set_page_config(page_title="AI Music Generator 🎵", layout="centered")
st.title("🎼 Fast AI Music Generator")
st.markdown("Generate random melodies in seconds — no deep learning model required!")
st.image("AIMG.png", caption="AI creating music", use_container_width=True)

# Function to generate a simple random melody

def generate_melody(scale_notes, length=8, tempo=120):
    melody = np.random.choice(scale_notes, size=length)
    return melody

# Function to create a MIDI file from melody
def save_midi(melody, tempo=120, file_name="output.mid"):
    midi = MIDIFile(1)  # 1 track
    track = 0
    time_ = 0
    channel = 0
    volume = 100
    duration = 1

    midi.addTempo(track, time_, tempo)

    for note in melody:
        midi.addNote(track, channel, note, time_, duration, volume)
        time_ += duration

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
        with open(tmp.name, "wb") as f:
            midi.writeFile(f)
        return tmp.name

# Define a simple C Major scale
scales = {
    "C Major": [60, 62, 64, 65, 67, 69, 71, 72],  # MIDI numbers
    "A Minor": [57, 59, 60, 62, 64, 65, 67, 69],
    "Pentatonic": [60, 62, 64, 67, 69, 72],
}

# User Inputs
scale_choice = st.selectbox("🎵 Choose a scale:", list(scales.keys()))
length = st.slider("🎚️ Length of melody (notes)", 4, 32, 8)
tempo = st.slider("⏱️ Tempo (BPM)", 60, 180, 120)

if st.button("🎶 Generate Melody"):
    with st.spinner("Composing your melody..."):
        melody = generate_melody(scales[scale_choice], length, tempo)
        midi_file_path = save_midi(melody, tempo)
        st.success("✅ Melody generated!")

        # MIDI Player (uses HTML5 audio player)
        audio_file_path = midi_file_path.replace(".mid", ".wav")

        # Convert to WAV using simple system tool (optional)
        try:
            from pydub import AudioSegment
            sound = AudioSegment.from_file(midi_file_path, format="mid")
            sound.export(audio_file_path, format="wav")
            st.audio(audio_file_path, format="audio/wav")
        except:
            st.warning("Unable to preview audio (missing pydub or ffmpeg). Download MIDI below instead.")

        st.download_button("⬇️ Download MIDI", open(midi_file_path, "rb"), file_name="ai_melody.mid")
