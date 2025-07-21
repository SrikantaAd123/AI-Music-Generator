import streamlit as st
from music_utils import generate_music

st.image("AIMG.png", caption="AI creating music", use_container_width=True)


st.set_page_config(page_title="AI Music Generator", layout="wide")

st.title("🎵 AI Music Generator")
prompt = st.text_input("Enter your music description prompt (e.g., Lo-fi chill with rain):")

if st.button("Generate"):
    with st.spinner("Composing your track..."):
        audio_file = generate_music(prompt)
        st.audio(audio_file, format="audio/wav")
        st.success("Here's your generated music!")
