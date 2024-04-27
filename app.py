import streamlit as st
from st_audiorec import st_audiorec




def welcomePage():
    st.title("CSC-480 Final Project\nBy: Noor Dhaliwal, Matthew Le,and Jeremiah Liao")
    # write a project introduction here

    if(st.button("Next")):
        st.session_state.page = "voiceInput"
        st.rerun()

def voiceInput():
    st.title("Voice Input")
    st.write("Click Begin Recording Audio, then say some words for a few seconds, for example you can say 'The quick brown fox jumped over the lazy dog.'")
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')

    if(st.button("Back")):
        st.session_state.page = "Welcome"
        st.rerun()

    

def main():
    page = st.session_state.get("page", "Welcome")
    if page == "Welcome":
        welcomePage()
    if page == "voiceInput":
        voiceInput()

if __name__ == '__main__':
    main()