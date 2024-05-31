import streamlit as st
from st_audiorec import st_audiorec
from chatwithai import streamlit_call_chatbot
from voiceEmbeddings import checkSimilarity, saveNew

import wave
import numpy as np

def save_wav(audio_data, filename):
    # Assuming audio_data is in the form of a NumPy array
    sample_rate = 44100  # You can change this based on your sample rate
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # Sample width in bytes
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())


def welcomePage():
    st.title("CSC-480 Final Project\nBy: Noor Dhaliwal, Matthew Le, and Jeremiah Liao")
    # write a project introduction here
    # st.write()
    if(st.button("Next")):
        st.session_state.page = "voiceInput"
        st.rerun()

def voiceInput():
    if "voiceID" not in st.session_state:
        st.session_state.voiceID = 0
    st.title("Voice Input")
    st.write("Click Begin Recording Audio, then say some words for a few seconds, for example you can say 'The quick brown fox jumped over the lazy dog.'")
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')

        filename = 'recorded_audio.wav'
        save_wav(np.array(wav_audio_data), filename)

        nearestNeighbors = checkSimilarity(wavData=filename)
        if not nearestNeighbors or all(similarity < 0.5 for similarity in nearestNeighbors.values()):
            st.write("No similar voice found. Initializing new user.")
            name = st.text_input("What is your name?")
            if(st.button("Save My Voice!")):
                saveNew(name, filename)
                clear_cache()
                st.rerun()

        else:
            st.write(nearestNeighbors)
            st.session_state.voiceID = list(nearestNeighbors.keys())[0]
                

    if(st.button("Back")):
        st.session_state.page = "Welcome"
        st.rerun()

    if(st.button("Next")):
        st.session_state.page = "chatWithAI"
        st.rerun()

def chatWithAI():
    st.title("Chat With AI")
    st.write("Type anything into the textbox below in order to start your conversation with the AI!")
    st.write("Once you're done, press the 'End Conversation' button to end the conversation and refresh the page!")

    streamlit_call_chatbot(st.session_state.voiceID)


def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)
    
def main():
    page = st.session_state.get("page", "Welcome")
    if page == "Welcome":
        welcomePage()
    if page == "voiceInput":
        voiceInput()
    if page == "chatWithAI":
        chatWithAI()

if __name__ == '__main__':
    main()