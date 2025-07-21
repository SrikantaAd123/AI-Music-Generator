from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from transformers import pipeline
from pydub.generators import Sine
from pydub import AudioSegment
import random

app = Flask(__name__)
CORS(app)

st.image("AIMG.png", caption="AI creating music", use_container_width=True)


# Dummy pipeline for example (replace with actual music generation model if available)
music_gen = pipeline("text-generation", model="gpt2")



@app.route("/generate-music", methods=["POST"])
def generate_music():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "Relaxing music")

        # Simulate AI response
        result = music_gen(prompt, max_length=30, do_sample=True)[0]['generated_text']

        # Use generated result to create fake audio
        frequency = 440 + random.randint(-50, 50)  # vary tone based on output
        duration_ms = 3000  # 3 seconds
        tone = Sine(frequency).to_audio_segment(duration=duration_ms)

        # Add a fade in/out effect
        tone = tone.fade_in(200).fade_out(200)

        # Save audio to a temporary file
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, "music.wav")
        tone.export(filename, format="wav")

        return send_file(filename, mimetype="audio/wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "🎵 AI Music Generator Flask API is Running! Use /generate-music endpoint."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
