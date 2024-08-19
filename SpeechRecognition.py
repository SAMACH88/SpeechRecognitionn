import streamlit as st
import speech_recognition as sr
import pyaudio
import pickle

# Load the pickled speech recognition data (recognizer, APIS, LANGUAGES)
with open('speech_recognition.pkl', 'rb') as f:
    faces_data = pickle.load(f)
# Initialize recognizer
recognizer = sr.Recognizer()

# Available speech recognition APIs
APIS = {
    "Google Web Speech API": "google",
    "Sphinx (Offline)": "sphinx"
}

# Supported languages
LANGUAGES = {
    "English": "en-US",
    "Arabic": "ar-SA",
    "German": "de-DE",
    "Spanish": "es-ES",
    "French": "fr-FR"
}


def check_audio_input_device():
    try:
        p = pyaudio.PyAudio()
        if p.get_default_input_device_info():
            return "Input device is available."
        else:
            return "No Default Input Device Available."
    except IOError:
        return "No Default Input Device Available."


def transcribe_speech(api_choice, language):
    try:
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)

        st.write("Processing...")

        # Select the API based on user's choice
        if api_choice == "google":
            return recognizer.recognize_google(audio, language=language)
        elif api_choice == "sphinx":
            return recognizer.recognize_sphinx(audio)
        else:
            return "Selected API not supported."
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from the API; {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    st.title("Speech Recognition App")

    # Check audio input device availability
    st.write(check_audio_input_device())

    # Select API
    api_choice = st.selectbox("Select Speech Recognition API", list(APIS.keys()))

    # Select language
    language_choice = st.selectbox("Select Language", list(LANGUAGES.keys()))
    selected_language = LANGUAGES[language_choice]

    # Start listening and transcribing
    if st.button("Start Listening"):
        transcribed_text = transcribe_speech(APIS[api_choice], selected_language)
        st.write("Transcribed Text:", transcribed_text)

        # Option to save the transcribed text
        if transcribed_text:
            if st.button("Save Transcription"):
                with open("transcription.txt", "w") as f:
                    f.write(transcribed_text)
                st.success("Transcription saved as 'transcription.txt'")
                with open("transcription.txt", "rb") as f:
                    st.download_button(label="Download Transcription", data=f, file_name="transcription.txt")

    # Pause functionality (if you plan to implement it)
    if st.button("Pause Listening"):
        st.write("Paused. Click 'Start Listening' to resume.")


if __name__ == "__main__":
    main()
