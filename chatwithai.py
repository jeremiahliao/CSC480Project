from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
import json



def streamlit_call_chatbot(voiceID):
    load_dotenv()

    st.write(f"Your Voice ID: {voiceID}")
    USER_AVATAR = "👤"
    BOT_AVATAR = "🤖"
    api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"



    def get_chat_history_file():
        return f"chat_history_{voiceID}.json"



    def load_chat_history():
        try:
            with open(get_chat_history_file(), "r") as file:
                return json.load(file)
        except FileNotFoundError:
            st.write(f"No existing chat history for voiceID: {voiceID}")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON for voiceID: {voiceID}")
            return []
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []



    def save_chat_history(messages):
        try:
            with open(get_chat_history_file(), "w") as file:
                json.dump(messages, file, indent=4)
                st.write(f"Chat history saved for voiceID: {voiceID}")
        except Exception as e:
            print(f"Error saving chat history: {e}")



    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()


    with st.sidebar:
        if st.button("Delete Chat History"):
            st.session_state.messages = []
            save_chat_history([])
            ##UPDATE THIS##


    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state["messages"],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


    if st.button("End Conversation"):
        save_chat_history(st.session_state.messages)

        ##FIX THIS##
        st.rerun()
