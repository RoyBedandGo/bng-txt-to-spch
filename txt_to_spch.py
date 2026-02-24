import streamlit as st
import asyncio
import edge_tts
import os

# --- Async Function for Edge TTS ---
async def generate_audio(text, voice, rate, output_filename):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(output_filename)

# --- Streamlit UI ---
st.title("BNG TEXT TO SPEECH GENERATION")
st.write("Generate text-to-speech audio and download the result.")

default_text = "Hello"

# 1. Text Input
text_input = st.text_area("Enter Text:", value=default_text, height=150)

# 2. Voice Selection 
voice_input = st.selectbox(
    "Select Voice:", 
    [
        "ja-JP-NanamiNeural", 
        "ja-JP-KeitaNeural",  
        "en-US-AriaNeural",   
        "en-US-GuyNeural"     
    ]
)

# 3. Speech Rate Slider
rate_percentage = st.slider("Speech Rate Adjustment (%)", min_value=-50, max_value=50, value=15)
rate_str = f"+{rate_percentage}%" if rate_percentage >= 0 else f"{rate_percentage}%"

# --- Generation Logic ---
if st.button("Generate Audio", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text to generate audio.")
    else:
        with st.spinner("Generating audio..."):
            output_file = "output_audio.mp3"
            
            try:
                # Run the async TTS function
                asyncio.run(generate_audio(text_input, voice_input, rate_str, output_file))
                
                # Read the generated audio file into memory
                with open(output_file, "rb") as file:
                    audio_bytes = file.read()
                
                st.success("Audio generated successfully!")
                
                # Play the sound in the browser
                st.audio(audio_bytes, format="audio/mp3")
                
                # Explicit Download Button
                st.download_button(
                    label="Download Audio ⬇️",
                    data=audio_bytes,
                    file_name="my_tts_audio.mp3",
                    mime="audio/mp3"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")