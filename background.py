import streamlit as st
import base64
import pyttsx3  # 🎙️ Text-to-speech
import speech_recognition as sr  # 🎤 Speech recognition
import time

# 🌟 Title
st.title("🔥 Streamlit with Local Background, TTS & Speech Recognition 🔥")

# 🖼️ Local image path
image_path = r"C:\Users\sunim\coding fellas\streamlit\ok.jpg"

# 🛠️ Function to load image as base64
def get_base64_image(image_path):
    """Load image and convert it to base64 format."""
    with open(image_path, "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode()
    return base64_str

# 🌟 Apply background image
def set_background(image_path):
    """Set the background image with base64 encoding."""
    try:
        img_base64 = get_base64_image(image_path)
        background_image = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(background_image, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"❌ Image not found at: {image_path}")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# 🎙️ Text-to-speech (TTS)
def speak(text, rate=170, volume=0.9):
    """Convert text to speech."""
    engine = pyttsx3.init()
    
    # 🎚️ Configure voice properties
    engine.setProperty("rate", rate)  # Speed
    engine.setProperty("volume", volume)  # Volume

    # 🔥 Ensure female voice if available
    female_voice = None
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.id.lower():
            female_voice = voice.id
            break

    if female_voice:
        engine.setProperty("voice", female_voice)

    # 🎤 Speak the text
    engine.say(text)
    engine.runAndWait()

# 🎤 Speech recognition
def recognize_speech():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=10)
            st.success("🔎 Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write(f"🗨️ You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("🤖 Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            st.error("⚠️ Couldn't connect to the recognition service.")
            return ""
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return ""

# 🌟 Set background
set_background(image_path)

# 🎯 UI Elements
name = st.text_input("Enter your name", placeholder="Type here...")

# 🎙️ Buttons
if st.button("🔊 Text-to-Speech"):
    if name:
        speak(f"Hello, {name}! Welcome to the Streamlit App.")
    else:
        st.warning("⚠️ Please enter your name first!")

if st.button("🎤 Speech Recognition"):
    result = recognize_speech()
    if result:
        st.success(f"✅ You said: {result}")

# 🌟 Footer
st.markdown("---")
st.markdown("✨ Made with ❤️ by Akhil Sir")

# 🕒 Add a subtle delay for smoother UI updates
time.sleep(0.5)
