import streamlit as st
from st_audiorec import st_audiorec
from chatbot import chat_with_AI
from chatwithai import streamlit_call_chatbot

def welcomePage():
    st.title("CSC-480 Final Project\nBy: Noor Dhaliwal, Matthew Le, and Jeremiah Liao")
    # write a project introduction here
    # st.write()

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

    if(st.button("Next")):
        st.session_state.page = "chatWithAI"
        st.rerun()

def chatWithAI():
    st.title("Chat With AI")
    st.write("Type anything into the textbox below in order to start your conversation with the AI!")
    st.write("Once you're done, press the 'End Conversation' button to end the conversation and refresh the page!")

    streamlit_call_chatbot()
    
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